import React from "react";
import { Alert } from "react-bootstrap";
import { isDefined } from "../util";
import "../App.scss";

export default function AlertBox({ err, setShow, errMsg, variant }) {
  return (
    <>
      <Alert
        className="w-75 d-flex flex-column"
        variant={variant}
        onClose={() => setShow(false)}
      >
        <Alert.Heading>
          {variant === "danger" ? "Oh snap! You got an error!" : "Success!"}
        </Alert.Heading>
        {err.length !== 0 && variant === "danger" ? (
          <h5>Please update the following incorrect fields:</h5>
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
