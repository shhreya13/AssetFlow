import api from "./api";

export const loginUser = async (email, password) => {
  const response = await api.post("/users/login", {
    email,
    password,
  });

  return response.data;
};

export const registerUser = async (data) => {
  const response = await api.post("/users/register", data);
  return response.data;
};
