import { backToFronMsgtMap } from "../constants/errors";

export const backToFrontMsg = (back) => {
  const res = backToFronMsgtMap.find((mapping) => back === mapping.back);
  return res ? res.front : back;
};
