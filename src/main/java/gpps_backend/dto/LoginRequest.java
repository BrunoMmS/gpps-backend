package gpps_backend.dto;

public record LoginRequest(String email, String password) {
    public LoginRequest {
        if (email == null || email.trim().isEmpty()) {
            throw new IllegalArgumentException("Email is required");
        }
        if (password == null || password.trim().isEmpty()) {
            throw new IllegalArgumentException("Password is required");
        }
    }
}
//public class LoginRequest {
//    private String email;
//    private String password;
//
//    public LoginRequest(String email, String password) {
//        this.email = email;
//        this.password = password;
//    }
//
//    public String getEmail() { return email; }
//    public String getPassword() { return password; }
//
//    public boolean isValid() {
//        return email != null && !email.trim().isEmpty()
//                && password != null && !password.trim().isEmpty();
//    }
//}