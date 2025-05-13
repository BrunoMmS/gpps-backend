package gpps_backend.persistence;

import java.sql.Connection;
import java.sql.DriverManager;

public class ConnectionManager {
    private static Connection connection = null;

//    public static Connection getConnection() {
//        try {
//
//            // Class.forName("com.mysql.cj.jdbc.Driver");
//            //	conn = DriverManager.getConnection("jdbc:sqlite:mydatabase.db");
//            connection = DriverManager.getConnection();
//
//        }catch (Exception e) {
//            e.printStackTrace();
//        }
//        return connection;
//    }
}

//private void connectDatabase() {
//    try {
//        Connection conn = DriverManager.getConnection(
//                "jdbc:mysql://localhost:3306/tu_base", "root", "tu_password"
//        );
//        UsuarioDAO dao = new UsuarioDAO(conn);
//        loginService = new LoginService(dao);
//        registroService = new RegistroService(dao);
//    } catch (Exception e) {
//        JOptionPane.showMessageDialog(this, "Error de conexión: " + e.getMessage());
//        System.exit(1);
//    }
//}