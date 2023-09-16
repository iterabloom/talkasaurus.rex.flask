import React, { useState, createContext, useContext, useEffect } from "react";
import io from "socket.io-client";

export const SocketContext = createContext();

export const SocketProvider = ({ children }) => {
  const [socket, setSocket] = useState();
  const socketUrl = process.env.REACT_APP_SERVER_URL || "http://localhost:5000";

  useEffect(() => {
    setSocket(io(socketUrl));
  }, [socketUrl]);

  return (
    <SocketContext.Provider value={socket}>
      {children}
    </SocketContext.Provider>
  );
};

export const useSocket = () => useContext(SocketContext);