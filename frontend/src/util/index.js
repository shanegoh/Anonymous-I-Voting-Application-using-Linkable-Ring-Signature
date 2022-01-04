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

export const setAreaID = (area_id) => {
  localStorage.setItem("AREA_ID", area_id);
};

export const getAreaID = () => {
  localStorage.getItem("AREA_ID");
};

export const removeAreaID = () => {
  localStorage.removeItem("AREA_ID");
};

export const ADMIN_ROLE = 0;
export const VOTER_ROLE = 1;

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

export const dateFormat = (date) => {
  return new Intl.DateTimeFormat("en-GB", {
    dateStyle: "medium",
    timeStyle: "medium",
  }).format(date);
};

export const dateFormatTwo = (date) => {
  return new Intl.DateTimeFormat("en-GB", {
    timeStyle: "long",
  }).format(date);
};

export const dateFormatForVoter = (date) => {
  return new Intl.DateTimeFormat("en-GB", {
    dateStyle: "medium",
    timeStyle: "medium",
  }).format(date);
};

export const DEFAULTSELECTOR = "DEFAULT";
export const DANGER = "danger";
export const SUCCESS = "success";
export const INFO = "info";
export const INVALID_FILE_TYPE = "Invalid File Type";
// "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8";
export const fileType =
  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
export const imageType = "image/png";
export const fileExtension = ".xlsx";
export const ELECTED = "Elected";
export const NOTELECTED = "Not Elected";
export const SAMPLE_EXCEL_DATA = [
  {
    email: "example@sg.gov",
    area_id: "YOUR_AREA_ID",
  },
];
