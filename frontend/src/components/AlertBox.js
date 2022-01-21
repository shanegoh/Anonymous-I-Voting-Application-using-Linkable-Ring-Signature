import React from "react";
import { Alert } from "react-bootstrap";
import { isDefined } from "../util";
import "../App.scss";

export default function AlertBox({ err, setShow, errMsg, variant }) {
  return (
    <>
      <Alert
        className="error-box-width d-flex flex-column"
        variant={variant}
        onClose={() => setShow(false)}
      >
        <Alert.Heading className="fs-5">
          {variant === "danger" ? "Oh snap! You got an error!" : "Success!"}
        </Alert.Heading>
        {err.length !== 0 && variant === "danger" ? (
          <h6>Please update the following incorrect fields:</h6>
        ) : (
          <></>
        )}
        <p>{errMsg}</p>
        {err.map((object, i) => {
          return (
            <div>
              <p>
                {i + 1}. &nbsp; {object}
              </p>
            </div>
          );
        })}
      </Alert>
    </>
  );
}
