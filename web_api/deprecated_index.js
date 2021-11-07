/* -----     Initialise Firebase admin     ----- */
const admin = require("firebase-admin");
const serviceAccount = require("./serviceAccount.json");
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://bards-way.firebaseio.com",
});

/* -----     Initialise Firebase classic     ----- */
const credentials = require("./credentials.json");
const firebase = require("firebase");
firebase.initializeApp({
  apiKey: credentials.apiKey,
  authDomain: credentials.authDomain,
  projectId: credentials.projectId,
});

/* -----     Initialise Firebase database     ----- */
require("firebase/firestore");
const db = firebase.firestore();
const userDb = "user-database";

/* -----     Initialise stripe information     ----- */
const stripe = require("stripe")(
  "sk_test_51HjC2FLWDqabJ2rnleTT5RKWSdIT9iHffyD5vP1wSqkIboniZHWC0GD4Oq8osXoxzB85SCyyoYSuH25slCGOqcNK00MwIMe5nG"
);
const PRODUCT_ID = "prod_ILbxsVAa9wYcTv";
const PRICE_ID = "price_1HllFtLWDqabJ2rn5vRAjGsh";

/* -----     Initialise application     ----- */
const cors = require("cors");
const express = require("express");
const app = express();
app.use(cors());

app.use(express.json());

/* -----     Create routes     ----- */
app.post("/login", (req, res) => {
  try {
    firebase
      .auth()
      .signInWithEmailAndPassword(req.body.email, req.body.password)
      .then(() => {
        firebase
          .auth()
          .currentUser.getIdToken(true)
          .then(() => {
            userInfo = JSON.parse(JSON.stringify(firebase.auth().currentUser));
            db.collection(userDb)
              .doc(userInfo.uid)
              .update({
                token: userInfo.stsTokenManager.accessToken,
                refreshToken: userInfo.stsTokenManager.refreshToken,
                tokenExpirationDate: new Date(userInfo.stsTokenManager.expirationTime),
              })
              .then(() => {
                db.collection(userDb)
                  .doc(firebase.auth().currentUser.uid)
                  .get()
                  .then((doc) => {
                    if (doc.data().licenseExpirationDate !== null)
                      res
                        .status(200)
                        .json({
                          message: "Logged succesfully!",
                          expiration: `${new Date(
                            (doc.data().licenseExpirationDate.seconds + 3600) * 1000
                          ).toUTCString()}+1`,
                          emailVerified: firebase.auth().currentUser.emailVerified,
                          responseType: "OK",
                          errorType: null,
                        });
                    else
                      res
                        .status(200)
                        .json({
                          message: "Logged succesfully!",
                          expiration: "null",
                          emailVerified: firebase.auth().currentUser.emailVerified,
                          responseType: "OK",
                          errorType: null,
                        });
                  })
                  .catch((error) =>
                    res
                      .status(202)
                      .json({
                        error: error.message,
                        responseType: "Accepted",
                        errorType: "RetrievingUserDataError",
                      })
                  );
              })
              .catch((error) =>
                res
                  .status(202)
                  .json({
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
        db.collection(userDb)
          .doc(firebase.auth().currentUser.uid)
          .set({
            email: firebase.auth().currentUser.email,
            token: null,
            refreshToken: null,
            tokenExpirationDate: null,
            licenseActivationDate: null,
            licenseExpirationDate: null,
            licenseKey: null,
            isLicenseKeyAcivated: false,
            isAdmin: false,
            isNightModeEnabled: true,
            stripeId: customer.id,
          })
          .then(() =>
            firebase
              .auth()
              .currentUser.sendEmailVerification()
              .then(() =>
                res.status(201).json({ message: "Done.", responseType: "Created", errorType: null })
              )
              .catch((error) =>
                res
                  .status(202)
                  .json({ error: error.message, responseType: "Accepted", errorType: "emailSenderError" })
              )
          )
          .catch((error) =>
            res
              .status(202)
              .json({
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

app.get("/resetPassword", (req, res) => {
  try {
    if (firebase.auth().currentUser === null)
      return res.status(403).json({ error: "FORBIDDEN", responseType: "Forbidden", errorType: "forbidden" });
    else if (firebase.auth().currentUser.emailVerified === false)
      return res
        .status(403)
        .json({
          error: "FORBIDDEN",
          emailVerified: false,
          responseType: "Forbidden",
          errorType: "forbidden",
        });

    firebase
      .auth()
      .sendPasswordResetEmail(firebase.auth().currentUser.email)
      .then(() =>
        res
          .status(200)
          .json({
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
      return res
        .status(403)
        .json({
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
          res
            .status(200)
            .json({
              user: firebase.auth().currentUser.uid,
              isAdmin: true,
              responseType: "OK",
              errorType: null,
            });
        else
          res
            .status(200)
            .json({
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

app.get("/createKey", async (req, res) => {
  try {
    if (firebase.auth().currentUser === null)
      return res.status(403).json({ error: "FORBIDDEN", responseType: "Forbidden", errorType: "forbidden" });
    else if (firebase.auth().currentUser.emailVerified === false)
      return res
        .status(403)
        .json({
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

app.get("/license", async (req, res) => {
  if (firebase.auth().currentUser === null)
    return res.status(403).json({ error: "FORBIDDEN", responseType: "Forbidden", errorType: "forbidden" });
  else if (firebase.auth().currentUser.emailVerified === false)
    return res
      .status(403)
      .json({ error: "FORBIDDEN", emailVerified: false, responseType: "Forbidden", errorType: "forbidden" });

  try {
    const user = await db.collection(userDb).doc(firebase.auth().currentUser.uid).get();
    res.status(200).json({ license: user.data().licenseKey, responseType: "OK", errorType: null });
  } catch (error) {
    res.status(202).json({ error: error.message, responseType: "Accepted", errorType: "retrieveKeyError" });
  }
});

app.get("/deleteKey", async (req, res) => {
  try {
    if (firebase.auth().currentUser === null)
      return res.status(403).json({ error: "FORBIDDEN", responseType: "Forbidden", errorType: "forbidden" });
    else if (firebase.auth().currentUser.emailVerified === false)
      return res
        .status(403)
        .json({
          error: "FORBIDDEN",
          emailVerified: false,
          responseType: "Forbidden",
          errorType: "forbidden",
        });

    db.collection(userDb)
      .doc(firebase.auth().currentUser.uid)
      .update({ licenseKey: null })
      .then((doc) =>
        res
          .status(200)
          .json({
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
      return res
        .status(403)
        .json({
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
          return res
            .status(202)
            .json({
              error: `User ${firebase.auth().currentUser.uid} doesn't have a license key.`,
              isAdmin: true,
              responseType: "Accepted",
              errorType: "licenseKeyNotFound",
            });
        if (doc.data().isActivated === true)
          return res
            .status(202)
            .json({
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
      return res
        .status(403)
        .json({
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
      return res
        .status(403)
        .json({
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

  if (firebase.auth().currentUser === null)
    return res.status(403).json({ error: "FORBIDDEN", responseType: "Forbidden", errorType: "forbidden" });
  else if (firebase.auth().currentUser.emailVerified === false)
    return res
      .status(403)
      .json({ error: "FORBIDDEN", emailVerified: false, responseType: "Forbidden", errorType: "forbidden" });

  res
    .status(200)
    .json({
      name: product.name,
      price: `${price.unit_amount / 100}€`,
      image: product.images[0],
      responseType: "OK",
      errorType: null,
    });
});

app.post("/pay", async (req, res) => {
  if (firebase.auth().currentUser === null)
    return res.status(403).json({ error: "FORBIDDEN", responseType: "Forbidden", errorType: "forbidden" });
  else if (firebase.auth().currentUser.emailVerified === false)
    return res
      .status(403)
      .json({ error: "FORBIDDEN", emailVerified: false, responseType: "Forbidden", errorType: "forbidden" });
  if (req.body.paymentMethod === undefined || !Object.keys(req.body.paymentMethod).length)
    return res
      .status(400)
      .json({
        error: "Missing payment method.",
        responseType: "Bad request",
        errorType: "missingPaymentMethod",
      });

  try {
    const licenseKey = createLicenseKey();
    const price = await stripe.prices.retrieve(PRICE_ID);
    const user = await db.collection(userDb).doc(firebase.auth().currentUser.uid).get();
    let customer = await stripe.customers.retrieve(user.data().stripeId);
    let paymentIntend = await stripe.paymentIntents.create({
      amount: price.unit_amount,
      currency: price.currency,
      customer: customer.id,
      payment_method: req.body.paymentMethod.id,
      receipt_email: customer.email,
    });

    await db.collection(userDb).doc(firebase.auth().currentUser.uid).update({ licenseKey: licenseKey });
    customer = await stripe.customers.update(customer.id, { metadata: { licenseKey: licenseKey } });
    paymentIntend = await stripe.paymentIntents.update(paymentIntend.id, {
      description: `License key: ${licenseKey}`,
    });
    paymentIntend = await stripe.paymentIntents.confirm(paymentIntend.id);
    res.status(200).json({ licenseKey: customer.metadata.licenseKey, responseType: "OK", errorType: null });
  } catch (error) {
    res.status(202).json({ error: error.message, responseType: "Accepted", errorType: "paymentError" });
  }
});

/* -----     FUN FACTS     ----- */

app.put("/coffee", (req, res) => {
  try {
    if (firebase.auth().currentUser === null)
      return res.status(403).json({ error: "FORBIDDEN", responseType: "Forbidden", errorType: "forbidden" });
    else if (firebase.auth().currentUser.emailVerified === false)
      return res
        .status(403)
        .json({
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
      return res
        .status(403)
        .json({
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
      return res
        .status(403)
        .json({
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
      return res
        .status(403)
        .json({
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
