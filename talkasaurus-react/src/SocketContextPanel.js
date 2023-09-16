import React from "react";
import io from "socket.io-client";

const SocketContext = React.createContext();

export const SocketProvider = ({ children }) => {
  // initialising socket connection
  const socket = io(process.env.REACT_APP_SERVER_URL, {
    transports: ["websocket"],
    upgrade: false,
  });

  return (
    <SocketContext.Provider value={socket}>
      {children}
    </SocketContext.Provider>
  );
};

export const useSocket = () => React.useContext(SocketContext);