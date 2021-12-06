// import jwt_decode from "jwt-decode";
export const setAccessToken = (token) => {
  localStorage.setItem("ACCESS_TOKEN", token);
};

export const setIDToken = (token) => {
  localStorage.setItem("ID_TOKEN", token);
};

export const getIDToken = () => {
  return localStorage.getItem("ID_TOKEN");
};

export const removeAccessToken = () => {
  localStorage.removeItem("ACCESS_TOKEN");
};

// export const checkExpiry = (token) => {
//   if (token) {
//     const decodedToken = jwt_decode(token);
//     if (decodedToken.exp * 1000 < new Date().getTime()) return true;
//     else return false;
//   } else return false;
// };

// export const axiosConfig = {
//   withCredentials: true,
//   headers: {
//     Authorization: localStorage.getItem("TOKEN"),
//   },
// };
