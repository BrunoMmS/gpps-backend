package gpps_backend.model;

import java.time.LocalDateTime;
import java.util.Objects;
import java.util.UUID;

public class User {
    private String id;
    private String name;
    private String lastName;
    private String email;
    private String password;
    private Rol role;
    private boolean isActive;
    private LocalDateTime createdAt;

    public User(String name, String lastName, String email, String password, Rol role) {
        this.id = UUID.randomUUID().toString();
        this.name = name;
        this.lastName = lastName;
        this.email = email;
        this.password = password;
        this.role = role;
        this.isActive = true;
        this.createdAt = LocalDateTime.now();
    }

    // Constructor (Para registro sin ID)
    //public User(String name, String lastName, String email, String password) {
    //    this(java.util.UUID.randomUUID().toString(), name, lastName, email, password, Rol.USER);
    //}

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getLastName() { return lastName; }
    public void setLastName(String lastName) { this.lastName = lastName; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }

    public Rol getRole() { return role; }
    public void setRole(Rol role) { this.role = role; }

    public boolean isActive() { return isActive; }
    public void setActive(boolean active) { isActive = active; }

    public java.time.LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(java.time.LocalDateTime createdAt) { this.createdAt = createdAt; }

    public String getFullName() {
        return name + " " + lastName;
    }

//    public boolean hasRole(Rol role) {
//        return this.role == role;
//    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        User user = (User) o;
        return Objects.equals(id, user.id) && Objects.equals(email, user.email);
    }

//    @Override
//    public int hashCode() {
//        return Objects.hash(id, email);
//    }

    @Override
    public String toString() {
        return "User{" +
                "id='" + id + '\'' +
                ", fullName='" + getFullName() + '\'' +
                ", email='" + email + '\'' +
                ", role=" + role +
                ", isActive=" + isActive +
                ", createdAt=" + createdAt +
                '}';
    }
}