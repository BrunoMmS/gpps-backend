package gpps_backend.ui;

import javax.swing.*;
import java.awt.*;

public class LoginUI extends JFrame {
    private JTextField txtEmail;
    private JPasswordField txtPassword;
    private JButton btnLogin, btnRegister;


    public LoginUI() {
        setTitle("Login");
        setSize(400, 200);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        initComponents();
        connectDatabase();
    }

    private void initComponents() {
        setLayout(new GridLayout(4, 2));

        add(new JLabel("Email:"));
        txtEmail = new JTextField();
        add(txtEmail);

        add(new JLabel("Contraseña:"));
        txtPassword = new JPasswordField();
        add(txtPassword);

        btnLogin = new JButton("Iniciar Sesión");
        btnRegistro = new JButton("Registrarse");
        add(btnLogin);
        add(btnRegistro);

        btnLogin.addActionListener(e -> login());
        btnRegistro.addActionListener(e -> registro());
    }



    private void login() {
        try {
            Usuario u = loginService.login(txtEmail.getText(), new String(txtPassword.getPassword()));
            if (u != null) {
                JOptionPane.showMessageDialog(this, "Bienvenido " + u.getNombre() + " (" + u.getRol() + ")");
            } else {
                JOptionPane.showMessageDialog(this, "Credenciales incorrectas.");
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    private void registro() {
        String nombre = JOptionPane.showInputDialog("Nombre completo:");
        String email = txtEmail.getText();
        String pass = new String(txtPassword.getPassword());
        Rol rol = (Rol) JOptionPane.showInputDialog(this, "Rol:", "Seleccionar rol",
                JOptionPane.QUESTION_MESSAGE, null, Rol.values(), Rol.ESTUDIANTE);
        try {
            if (registroService.registrar(nombre, email, pass, rol)) {
                JOptionPane.showMessageDialog(this, "Registro exitoso");
            } else {
                JOptionPane.showMessageDialog(this, "Email ya registrado");
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new LoginUI().setVisible(true));
    }
}

