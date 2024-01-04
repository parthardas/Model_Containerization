import axios from "axios";

const createAxios = () => {
  const config = {};
  config.baseURL = process.env.REACT_APP_BASE_URL;
  const axiosInstance = axios.create(config);

  axiosInstance.interceptors.response.use(
    (response) => response,
    (error) => {
      // const errorResponse = error.response;
      // const errors = displayErrors(errorResponse);
      // errors.map((error) => {
      //   console.log(error);
      //   //   add error snackbar
      //   //   message.error(error);
      // });
      return Promise.reject(error);
    }
  );

  const get = ({ url, params }) =>
    axiosInstance.request({
      method: "GET",
      url,
      params,
    });

  const post = ({ url, data, config = {} }) =>
    axiosInstance.request({
      method: "POST",
      url,
      data,
      ...config,
    });

  const put = ({ url, data, config = {} }) =>
    axiosInstance.request({
      method: "PUT",
      url,
      data,
      ...config,
    });

  const remove = ({ url, data, config = {} }) =>
    axiosInstance.request({
      method: "DELETE",
      url,
      data,
      ...config,
    });

  return {
    instance: axiosInstance,
    get,
    post,
    put,
    delete: remove,
  };
};

export default createAxios;
