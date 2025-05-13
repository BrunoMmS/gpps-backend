package gpps_backend.dto;

public record RegisterRequest(
        String firstName,
        String lastName,
        String email,
        String password,
        String confirmPassword
) {
    public RegisterRequest {
        if (firstName == null || firstName.trim().isEmpty()) {
            throw new IllegalArgumentException("First name is required");
        }
        if (lastName == null || lastName.trim().isEmpty()) {
            throw new IllegalArgumentException("Last name is required");
        }
        if (email == null || email.trim().isEmpty()) {
            throw new IllegalArgumentException("Email is required");
        }
        if (password == null || password.trim().isEmpty()) {
            throw new IllegalArgumentException("Password is required");
        }
        if (!password.equals(confirmPassword)) {
            throw new IllegalArgumentException("Passwords do not match");
        }
    }
}

//public class RegisterRequest {
//    private String firstName;
//    private String lastName;
//    private String email;
//    private String password;
//    private String confirmPass;
//
//    public RegisterRequest(String firstName, String lastName, String email,
//                           String password, String confirmPass) {
//        this.firstName = firstName;
//        this.lastName = lastName;
//        this.email = email;
//        this.password = password;
//        this.confirmPass = confirmPass;
//    }
//
//    // Getters
//    public String getFirstName() { return firstName; }
//    public String getLastName() { return lastName; }
//    public String getEmail() { return email; }
//    public String getPassword() { return password; }
//    public String getConfirmPass() { return confirmPass; }
//
//    // Validaciones
//    public java.util.List<String> validate() {
//        java.util.List<String> errors = new java.util.ArrayList<>();
//
//        if (firstName == null || firstName.trim().isEmpty()) {
//            errors.add(NAME_VALID);
//        }
//
//        if (lastName == null || lastName.trim().isEmpty()) {
//            errors.add(LNAME_VALID);
//        }
//
//        if (email == null || email.trim().isEmpty()) {
//            errors.add(EMAIL_VALID);
//        } else if (!isValidEmail(email)) {
//            errors.add(EMAIL_FORMAT_VALID);
//
//        }
//
//        if (password == null || password.trim().isEmpty()) {
//            errors.add(PASS_VALID);
//        } else if (password.length() < 8) {
//            errors.add(PASS_MIN_CHAR);
//        } else if (!hasValidPasswordComplexity(password)) {
//            errors.add(PASS_ADVICE);
//        }
//
//        if (!password.equals(confirmPass)) {
//            errors.add(PASS_NOT_COINCIDE);
//        }
//
//        return errors;
//    }
//
//    private boolean isValidEmail(String email) {
//        return email.matches("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$");
//    }
//
//    private boolean hasValidPasswordComplexity(String password) {
//        return password.matches(".*[a-zA-Z].*") && password.matches(".*\\d.*");
//    }
//
//    public boolean isValid() {
//        return validate().isEmpty();
//    }
//
//    public static final String NAME_VALID = "El nombre es obligatorio";
//    public static final String LNAME_VALID = "El apellido es obligatorio";
//    public static final String EMAIL_VALID = "El email es obligatorio";
//    public static final String EMAIL_FORMAT_VALID = "El formato del email no es válido";
//    public static final String PASS_VALID = "La contraseña es obligatoria";
//    public static final String PASS_MIN_CHAR = "La contraseña debe tener al menos 8 caracteres";
//    public static final String PASS_ADVICE = "La contraseña debe contener al menos una letra y un número";
//    public static final String PASS_NOT_COINCIDE = "Las contraseñas no coinciden";
//
//}