import createAxios from "./createAxios";

const browserAxios = createAxios();

export const addNewUser =
  (axios = browserAxios) =>
  (data) =>
    axios.post({ url: "/add_user_details", data });

export const getCreditScoreById =
  (axios = browserAxios) =>
  (data) =>
    axios.get({ url: `/get_credit_score?customer_id=${data.customer_id}` });

export const getCreditScore =
  (axios = browserAxios) =>
  (data) =>
    axios.post({ url: `/get_credit_score`, data });
