export const types = {
  updateUser: "UPDATE_USER",
  updateLicense: "UPDATE_LICENSE",
};

const Reducer = (state, action) => {
  switch (action.type) {
    case types.updateUser:
      return {
        ...state,
        user: action.payload.user,
      };
    case types.updateLicense:
      return {
        ...state,
        user: state.user ? { ...state.user, licenseKey: action.payload.licenseKey } : state.user,
      };
    default:
      return state;
  }
};

export default Reducer;
