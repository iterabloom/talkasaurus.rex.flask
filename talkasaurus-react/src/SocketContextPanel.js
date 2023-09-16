import React, { createContext, useContext, useEffect, useState } from "react";
import io from "socket.io-client";

//Creating Socket context
export const SocketContext = createContext();

//This component provides the socket context to its children
export const SocketProvider = ({ children }) => {
  const [socket, setSocket] = useState();
  const socketUrl = process.env.REACT_APP_SERVER_URL || "http://localhost:5000";

  //Instantiation of socket object
  useEffect(() => {
    setSocket(io(socketUrl));
  }, [socketUrl]);

  return (
    <SocketContext.Provider value={socket}>
      {children}
    </SocketContext.Provider>
  );
};

//Hook for socket context
export const useSocket = () => useContext(SocketContext);