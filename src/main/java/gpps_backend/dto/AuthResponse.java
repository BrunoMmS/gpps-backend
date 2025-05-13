package gpps_backend.dto;

import gpps_backend.model.User;

public sealed interface AuthResponse permits AuthResponse.Success, AuthResponse.Failure{
    record Success(User user, String message) implements AuthResponse {
        public Success(User user) {
            this(user, "Authentication successful");
        }
    }

    record Failure(String error, String details) implements AuthResponse {
        public Failure(String error) {
            this(error, null);
        }
    }
}
