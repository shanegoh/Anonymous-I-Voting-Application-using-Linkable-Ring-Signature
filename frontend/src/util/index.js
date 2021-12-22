// import jwt_decode from "jwt-decode";
export const setAccessToken = (token) => {
  localStorage.setItem("ACCESS_TOKEN", token);
};

export const setIDToken = (token) => {
  localStorage.setItem("ID_TOKEN", token);
};

export const removeAccessToken = () => {
  localStorage.removeItem("ACCESS_TOKEN");
};

export const removeIDToken = () => {
  localStorage.removeItem("ID_TOKEN");
};

export const getAccessToken = () => {
  return localStorage.getItem("ACCESS_TOKEN");
};

export const getIDToken = () => {
  return localStorage.getItem("ID_TOKEN");
};

export const setRoleID = (role_id) => {
  localStorage.setItem("ROLE_ID", role_id);
};

export const removeRoleID = () => {
  localStorage.removeItem("ROLE_ID");
};

export const isAdmin = () => {
  return localStorage.getItem("ROLE_ID") === "0" ? true : false;
};

export const admin_role = 0;
export const voter_role = 1;

// export const checkExpiry = (token) => {
//   if (token) {
//     const decodedToken = jwt_decode(token);
//     if (decodedToken.exp * 1000 < new Date().getTime()) return true;
//     else return false;
//   } else return false;
// };

export const axiosConfig = {
  headers: {
    Authorization: `Bearer ${localStorage.getItem("ACCESS_TOKEN")}`,
    id_token: `Bearer ${localStorage.getItem("ID_TOKEN")}`,
  },
};

// A function to check for undefined value
export const isDefined = (value) => {
  return typeof value !== "undefined";
};
