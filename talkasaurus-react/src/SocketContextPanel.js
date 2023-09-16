import React from "react";
import io from "socket.io-client";

const SocketContext = React.createContext();

export const SocketProvider = ({ children }) => {
  const socketURL = process.env.REACT_APP_SERVER_URL;

  const [socket, setSocket] = useState()

  useEffect(() => {
    setSocket(io(socketURL));
  }, [socketURL])

  return (
    <SocketContext.Provider value={socket}>
      {children}
    </SocketContext.Provider>
  );
};

export const useSocket = () => React.useContext(SocketContext);