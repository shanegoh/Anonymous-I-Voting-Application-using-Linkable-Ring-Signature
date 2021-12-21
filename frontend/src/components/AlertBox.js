import React from "react";
import { Alert } from "react-bootstrap";
import "../App.scss";

export default function AlertBox({ err, setShow, errMsg }) {
  return (
    <>
      <Alert
        className="w-75 d-flex flex-column"
        variant="danger"
        onClose={() => setShow(false)}
        dismissible
      >
        <Alert.Heading>Oh snap! You got an error!</Alert.Heading>
        {err.length !== 0 ? (
          <h5>Please update the following incorrect fields:</h5>
        ) : (
          <></>
        )}
        {typeof errMsg !== "undefined" ? <p>{errMsg}</p> : <></>}

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
