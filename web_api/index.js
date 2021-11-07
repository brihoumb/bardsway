/* -----     Initialise Firebase admin     ----- */
const admin = require("firebase-admin");
const serviceAccount = require("./serviceAccount.json");
const credentials = require("./credentials.json");
const firebase = require("firebase");
require("firebase/firestore");
const cors = require("cors");
const express = require("express");
const stripe = require("stripe")(
  "sk_test_51HjC2FLWDqabJ2rnleTT5RKWSdIT9iHffyD5vP1wSqkIboniZHWC0GD4Oq8osXoxzB85SCyyoYSuH25slCGOqcNK00MwIMe5nG"
);

firebase.initializeApp({
  apiKey: credentials.apiKey,
  authDomain: credentials.authDomain,
  projectId: credentials.projectId,
});

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://bards-way.firebaseio.com",
});

const db = firebase.firestore();
const userDb = "user-database";

const PRODUCT_ID = "prod_ILbxsVAa9wYcTv";
const PRICE_ID = "price_1HwG9GLWDqabJ2rnKQfb8Ljh";

const createLicenseKey = () => {
  let res = "BW-";
  Array.from({ length: 20 }, () => Math.floor(Math.random() * 24)).forEach((index, increment) => {
    res += "ACDEFGHJKLMNPQRTWXY34679"[index];
    if ((increment + 1) % 5 === 0 && increment !== 19) {
      res += "-";
    }
  });
  return res;
};

const sendableUser = async (uid) => {
  const { email, licenseKey, licenseExpirationDate } = await (await db.collection(userDb).doc(uid).get()).data();
  if (licenseExpirationDate !== null)
	return { email, licenseKey, licenseExpirationDate: licenseExpirationDate.seconds };
  return { email, licenseKey, licenseExpirationDate };
};

const app = express();
app.use(cors());
app.use(express.json());

app.get("/user", async (req, res) => {
  // success: {user: { email }}
  try {
    const user = firebase.auth().currentUser;
    if (!user)
      return res
        .status(403)
        .json({ error: "Not logged in", responseType: "Forbidden", errorType: "notLogged" });
    return res.status(200).json({ user: await sendableUser(user.uid) });
  } catch (e) {
    return res.status(400).json({ error: e.message, responseType: "Bad request", errorType: "badUserError" });
  }
});

app.post("/login", (req, res) => {
  try {
    firebase
      .auth()
      .signInWithEmailAndPassword(req.body.email, req.body.password)
      .then(() => {
        firebase
          .auth()
          .currentUser.getIdToken(true)
          .then((token) => {
            userInfo = JSON.parse(JSON.stringify(firebase.auth().currentUser));
            const { accessToken, refreshToken, expirationTime } = userInfo.stsTokenManager;
            const session = { accessToken, refreshToken, expirationTime };
            console.log({ token, session });
            db.collection(userDb)
              .doc(userInfo.uid)
              .update({ session })
              .then(() => {
                db.collection(userDb)
                  .doc(firebase.auth().currentUser.uid)
                  .get()
                  .then(async (doc) => {
                    const informations = await sendableUser(userInfo.uid);
                    res.status(200).json({
                      message: "Logged succesfully!",
                      emailVerified: firebase.auth().currentUser.emailVerified,
                      responseType: "OK",
                      errorType: null,
                      user: informations,
                      expiration: informations.licenseExpirationDate,
                    });
                  })
                  .catch((error) =>
                    res.status(202).json({
                      error: error.message,
                      responseType: "Accepted",
                      errorType: "RetrievingUserDataError",
                    })
                  );
              })
              .catch((error) =>
                res.status(202).json({
                  error: error.message,
                  responseType: "Accepted",
                  errorType: "ModifyingUserDocumentError",
                })
              );
          })
          .catch((error) =>
            res
              .status(202)
              .json({ error: error.message, responseType: "Accepted", errorType: "RefreshingUserTokenError" })
          );
      })
      .catch((error) =>
        res.status(401).json({ error: error.message, responseType: "Unauthorized", errorType: "SignInError" })
      );
  } catch (error) {
    res.status(400).json({ error: error.message, responseType: "Bad request", errorType: "badUserError" });
  }
});

app.post("/signup", (req, res) => {
  try {
    firebase
      .auth()
      .createUserWithEmailAndPassword(req.body.email, req.body.password)
      .then(async () => {
        const customer = await stripe.customers.create({ email: req.body.email });
        const user = firebase.auth().currentUser;
        db.collection(userDb)
          .doc(user.uid)
          .set({
            email: user.email,
            licenseActivationDate: null,
            licenseExpirationDate: null,
            licenseKey: null,
            isLicenseKeyAcivated: false,
            isAdmin: false,
            isNightModeEnabled: true,
            stripeId: customer.id,
          })
          .then(() =>
            user
              .sendEmailVerification()
              .then(async () =>
                res.status(201).json({
                  message: "Done.",
                  responseType: "Created",
                  errorType: null,
                  user: await sendableUser(user.uid),
                })
              )
              .catch(async (error) =>
                res.status(202).json({
                  error: error.message,
                  responseType: "Accepted",
                  errorType: "emailSenderError",
                  user: await sendableUser(user.uid),
                })
              )
          )
          .catch((error) =>
            res.status(202).json({
              error: error.message,
              responseType: "Accepted",
              errorType: "creatingUserDocumentError",
            })
          );
      })
      .catch((error) =>
        res
          .status(401)
          .json({ error: error.message, responseType: "Unauthorized", errorType: "creatingUserError" })
      );
  } catch (error) {
    res.status(400).json({ error: error.message, responseType: "Bad request", errorType: "badUserError" });
  }
});

app.get("/signout", async (req, res) => {
  try {
    await firebase.auth().signOut();
    return res.status(200).json({ user: null });
  } catch (e) {
    return res.status(400).json({ error: error.message });
  }
});

app.get("/resetPassword", (req, res) => {
  try {
    if (firebase.auth().currentUser === null)
      return res.status(403).json({ error: "FORBIDDEN", responseType: "Forbidden", errorType: "forbidden" });
    else if (firebase.auth().currentUser.emailVerified === false)
      return res.status(403).json({
        error: "FORBIDDEN",
        emailVerified: false,
        responseType: "Forbidden",
        errorType: "forbidden",
      });

    firebase
      .auth()
      .sendPasswordResetEmail(firebase.auth().currentUser.email)
      .then(() =>
        res.status(200).json({
          error: "Password user has been successfully reseted!",
          responseType: "OK",
          errorType: null,
        })
      )
      .catch((error) =>
        res
          .status(202)
          .json({ error: error.message, responseType: "Accepted", errorType: "resetPasswordError" })
      );
  } catch (error) {
    res.status(500).json({ error: error.message, responseType: "Internal error", errorType: "unknown" });
  }
});

app.get("/isAdmin", (req, res) => {
  try {
    if (firebase.auth().currentUser === null)
      return res.status(403).json({ error: "FORBIDDEN", responseType: "Forbidden", errorType: "forbidden" });
    else if (firebase.auth().currentUser.emailVerified === false)
      return res.status(403).json({
        error: "FORBIDDEN",
        emailVerified: false,
        responseType: "Forbidden",
        errorType: "forbidden",
      });

    db.collection(userDb)
      .doc(firebase.auth().currentUser.uid)
      .get()
      .then((doc) => {
        if (doc.data().isAdmin === true)
          res.status(200).json({
            user: firebase.auth().currentUser.uid,
            isAdmin: true,
            responseType: "OK",
            errorType: null,
          });
        else
          res.status(200).json({
            user: firebase.auth().currentUser.uid,
            isAdmin: false,
            responseType: "OK",
            errorType: null,
          });
      })
      .catch((error) =>
        res.status(202).json({ error: error.message, responseType: "Accepted", errorType: "adminCheckError" })
      );
  } catch (error) {
    res.status(500).json({ error: error.message, responseType: "Internal error", errorType: "unknown" });
  }
});

app.get("/createKey", async (req, res) => {
  try {
    if (firebase.auth().currentUser === null)
      return res.status(403).json({ error: "FORBIDDEN", responseType: "Forbidden", errorType: "forbidden" });
    else if (firebase.auth().currentUser.emailVerified === false)
      return res.status(403).json({
        error: "FORBIDDEN",
        emailVerified: false,
        responseType: "Forbidden",
        errorType: "forbidden",
      });

    const licenseKey = createLicenseKey();
    db.collection(userDb)
      .doc(firebase.auth().currentUser.uid)
      .update({ licenseKey: licenseKey })
      .then((doc) => res.status(200).json({ licenseKey: licenseKey, responseType: "OK", errorType: null }))
      .catch((error) =>
        res
          .status(202)
          .json({ error: error.message, responseType: "Accepted", errorType: "creatingKeyError" })
      );
  } catch (error) {
    res.status(500).json({ error: error.message, responseType: "Internal error", errorType: "unknown" });
  }
});

app.get("/deleteKey", async (req, res) => {
  try {
    if (firebase.auth().currentUser === null)
      return res.status(403).json({ error: "FORBIDDEN", responseType: "Forbidden", errorType: "forbidden" });
    else if (firebase.auth().currentUser.emailVerified === false)
      return res.status(403).json({
        error: "FORBIDDEN",
        emailVerified: false,
        responseType: "Forbidden",
        errorType: "forbidden",
      });

    db.collection(userDb)
      .doc(firebase.auth().currentUser.uid)
      .update({ licenseKey: null })
      .then((doc) =>
        res.status(200).json({
          message: `${firebase.auth().currentUser.uid} have revoke his licenseKey.`,
          responseType: "OK",
          errorType: null,
        })
      )
      .catch((error) =>
        res.status(202).json({ error: error.message, responseType: "Accepted", errorType: "deleteKeyError" })
      );
  } catch (error) {
    res.status(500).json({ error: error.message, responseType: "Internal error", errorType: "unknown" });
  }
});

app.get("/activateKey", (req, res) => {
  try {
    const today = new Date();
    const expiration = new Date(today.getFullYear() + 1, today.getMonth(), today.getDate());

    if (firebase.auth().currentUser === null)
      return res.status(403).json({ error: "FORBIDDEN", responseType: "Forbidden", errorType: "forbidden" });
    else if (firebase.auth().currentUser.emailVerified === false)
      return res.status(403).json({
        error: "FORBIDDEN",
        emailVerified: false,
        responseType: "Forbidden",
        errorType: "forbidden",
      });

    db.collection(userDb)
      .doc(firebase.auth().currentUser.uid)
      .get()
      .then((doc) => {
        if (doc.data().licenseKey === null)
          return res.status(202).json({
            error: `User ${firebase.auth().currentUser.uid} doesn't have a license key.`,
            isAdmin: true,
            responseType: "Accepted",
            errorType: "licenseKeyNotFound",
          });
        if (doc.data().isActivated === true)
          return res.status(202).json({
            error: `User ${firebase.auth().currentUser.uid} already activated his license key.`,
            isAdmin: true,
            responseType: "Accepted",
            errorType: "licenseAlreadyActivated",
          });
        db.collection(userDb)
          .doc(firebase.auth().currentUser.uid)
          .update({
            isActivated: true,
            licenseActivationDate: today,
            licenseExpirationDate: expiration,
          })
          .then((doc) =>
            res.status(200).json({ message: "License activated.", responseType: "OK", errorType: null })
          )
          .catch((error) =>
            res
              .status(202)
              .json({ error: error.message, responseType: "Accepted", errorType: "activatingKeyError" })
          );
      });
  } catch (error) {
    res.status(500).json({ error: error.message, responseType: "Internal error", errorType: "unknown" });
  }
});

app.get("/deactivateKey", (req, res) => {
  try {
    if (firebase.auth().currentUser === null)
      return res.status(403).json({ error: "FORBIDDEN", responseType: "Forbidden", errorType: "forbidden" });
    else if (firebase.auth().currentUser.emailVerified === false)
      return res.status(403).json({
        error: "FORBIDDEN",
        emailVerified: false,
        responseType: "Forbidden",
        errorType: "forbidden",
      });

    db.collection(userDb)
      .doc(firebase.auth().currentUser.uid)
      .update({
        isActivated: false,
        licenseActivationDate: null,
        licenseExpirationDate: null,
      })
      .then((doc) =>
        res.status(200).json({ message: "License deactivated.", responseType: "OK", errorType: null })
      )
      .catch((error) =>
        res
          .status(202)
          .json({ error: error.message, responseType: "Accepted", errorType: "deactivateKeyError" })
      );
  } catch (error) {
    res.status(500).json({ error: error.message, responseType: "Internal error", errorType: "unknown" });
  }
});

app.delete("/deleteUser", (req, res) => {
  try {
    if (firebase.auth().currentUser === null)
      return res.status(403).json({ error: "FORBIDDEN", responseType: "Forbidden", errorType: "forbidden" });
    else if (firebase.auth().currentUser.emailVerified === false)
      return res.status(403).json({
        error: "FORBIDDEN",
        emailVerified: false,
        responseType: "Forbidden",
        errorType: "forbidden",
      });

    db.collection(userDb)
      .doc(firebase.auth().currentUser.uid)
      .delete()
      .then(() => {})
      .catch((error) =>
        res
          .status(202)
          .json({ error: error.message, responseType: "Accepted", errorType: "documentDeletionError" })
      );
    firebase
      .auth()
      .currentUser.delete()
      .then(() =>
        res
          .status(200)
          .json({ message: "User has been successfully deleted!", responseType: "OK", errorType: null })
      )
      .catch((error) =>
        res
          .status(202)
          .json({ error: error.message, responseType: "Accepted", errorType: "userDeletionError" })
      );
  } catch (error) {
    res.status(500).json({ error: error.message, responseType: "Internal error", errorType: "unknown" });
  }
});

app.get("/product", async (req, res) => {
  const price = await stripe.prices.retrieve(PRICE_ID);
  const product = await stripe.products.retrieve(PRODUCT_ID);
  res.status(200).json({
    name: product.name,
    price: `${price.unit_amount / 100}€`,
    image: product.images[0],
    responseType: "OK",
    errorType: null,
  });
});

app.post("/postSignup", async (req, res) => {
  const { accessToken } = req.body;
  const { uid } = await admin.auth().verifyIdToken(accessToken);
  if (!uid)
    return res.status(403).json({ error: "FORBIDDEN", responseType: "Forbidden", errorType: "forbidden" });
  const user = await admin.auth().getUser(uid);
  const customer = await stripe.customers.create({ email: user.email });
  await db.collection(userDb).doc(uid).set({
    email: user.email,
    licenseActivationDate: null,
    licenseExpirationDate: null,
    licenseKey: null,
    isLicenseKeyAcivated: false,
    isAdmin: false,
    isNightModeEnabled: true,
    stripeId: customer.id,
  });
  return res.status(200).json({ error: null });
});

app.post("/pay", async (req, res) => {
  const { accessToken, paymentMethod } = req.body;
  const { uid } = await admin.auth().verifyIdToken(accessToken);
  if (!uid)
    return res.status(403).json({ error: "FORBIDDEN", responseType: "Forbidden", errorType: "forbidden" });
  const user = await admin.auth().getUser(uid);
  const userDoc = (await db.collection(userDb).doc(uid).get()).data();
  if (!user || !user.emailVerified) {
    return res
      .status(403)
      .json({ error: "FORBIDDEN", emailVerified: false, responseType: "Forbidden", errorType: "forbidden" });
  } else if (!paymentMethod)
    return res.status(400).json({
      error: "Missing payment method.",
      responseType: "Bad request",
      errorType: "missingPaymentMethod",
    });

  try {
    const licenseKey = createLicenseKey();
    const price = await stripe.prices.retrieve(PRICE_ID);
    let customer = null;
    if (!userDoc.stripeId) {
      customer = await stripe.customers.create({ email: user.email });
      await admin.auth().updateUser(uid, { stripeId: customer.id });
    } else customer = await stripe.customers.retrieve(userDoc.stripeId);

    let paymentIntend = await stripe.paymentIntents.create({
      amount: price.unit_amount,
      currency: price.currency,
      customer: customer.id,
      payment_method: paymentMethod.id,
      receipt_email: customer.email,
    });

    await db.collection(userDb).doc(uid).update({ licenseKey });
    customer = await stripe.customers.update(customer.id, { metadata: { licenseKey } });
    paymentIntend = await stripe.paymentIntents.update(paymentIntend.id, {
      description: `License key: ${licenseKey}`,
    });
    paymentIntend = await stripe.paymentIntents.confirm(paymentIntend.id);
    res.status(200).json({ licenseKey, responseType: "OK", errorType: null });
  } catch (error) {
    res.status(202).json({ error: error.message, responseType: "Accepted", errorType: "paymentError" });
  }
});

app.post("/license", async (req, res) => {
  try {
    const { accessToken } = req.body;
    const { uid } = await admin.auth().verifyIdToken(accessToken);
    if (!uid)
      return res.status(403).json({ error: "FORBIDDEN", responseType: "Forbidden", errorType: "forbidden" });
    // const user = await admin.auth().getUser(uid);
    const userDoc = (await db.collection(userDb).doc(uid).get()).data();
    console.log({ accessToken, uid, userDoc });
    if (!userDoc)
      return res.status(403).json({
        error: "FORBIDDEN",
        emailVerified: false,
        responseType: "Forbidden",
        errorType: "forbidden",
      });
    const { licenseKey } = userDoc;
    return res.status(200).json({ licenseKey });
  } catch (e) {
    res.status(401).json({ error: { type: "invalidToken", msg: "Access token verification failed" } });
  }
});

/* -----     FUN FACTS     ----- */

app.put("/coffee", (req, res) => {
  try {
    if (firebase.auth().currentUser === null)
      return res.status(403).json({ error: "FORBIDDEN", responseType: "Forbidden", errorType: "forbidden" });
    else if (firebase.auth().currentUser.emailVerified === false)
      return res.status(403).json({
        error: "FORBIDDEN",
        emailVerified: false,
        responseType: "Forbidden",
        errorType: "forbidden",
      });
    res.status(418).json({ message: "WAIT WHAT?!?!", responseType: "I'm a teapot", errorType: "teapot" });
  } catch (error) {
    res.status(500).json({ error: error.message, responseType: "Internal error", errorType: "unknown" });
  }
});

app.put("/gradeA", (req, res) => {
  try {
    if (firebase.auth().currentUser === null)
      return res.status(403).json({ error: "FORBIDDEN", responseType: "Forbidden", errorType: "forbidden" });
    else if (firebase.auth().currentUser.emailVerified === false)
      return res.status(403).json({
        error: "FORBIDDEN",
        emailVerified: false,
        responseType: "Forbidden",
        errorType: "forbidden",
      });
    res
      .status(417)
      .json({ message: "EN FAIT NON!", responseType: "Expectation failed", errorType: "expectationFailed" });
  } catch (error) {
    res.status(500).json({ error: error.message, responseType: "Internal error", errorType: "unknown" });
  }
});

app.put("/gradeE", (req, res) => {
  try {
    if (firebase.auth().currentUser === null)
      return res.status(403).json({ error: "FORBIDDEN", responseType: "Forbidden", errorType: "forbidden" });
    else if (firebase.auth().currentUser.emailVerified === false)
      return res.status(403).json({
        error: "FORBIDDEN",
        emailVerified: false,
        responseType: "Forbidden",
        errorType: "forbidden",
      });
    res
      .status(426)
      .json({ message: "OH RLY?!?!", responseType: "Upgrade required", errorType: "upgradeRequired" });
  } catch (error) {
    res.status(500).json({ error: error.message, responseType: "Internal error", errorType: "unknown" });
  }
});

app.put("/yacine", (req, res) => {
  try {
    if (firebase.auth().currentUser === null)
      return res.status(403).json({ error: "FORBIDDEN", responseType: "Forbidden", errorType: "forbidden" });
    else if (firebase.auth().currentUser.emailVerified === false)
      return res.status(403).json({
        error: "FORBIDDEN",
        emailVerified: false,
        responseType: "Forbidden",
        errorType: "forbidden",
      });
    res
      .status(410)
      .json({ message: "AAAAANNNNNNDDDDD... IT'S GONE!", responseType: "Gone", errorType: "gone" });
  } catch (error) {
    res.status(500).json({ error: error.message, responseType: "Internal error", errorType: "unknown" });
  }
});

/* -----     Error 404 handling     ----- */
app.all("*", (req, res) =>
  res
    .status(404)
    .json({ error: "Route or method not found", responseType: "Not found", errorType: "notFound" })
);

/* -----     Create server     ----- */
app.listen(8080, () => {
  console.log("Serveur à l'écoute");
});
