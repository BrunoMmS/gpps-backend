package gpps_backend.model;

public enum Rol {

    ADMIN(Constants.ADMIN, Constants.ADMIN_DASHBOARD),
    STUDENT(Constants.STUDENT, Constants.STUDENT_DASHBOARD),
    TUTOR(Constants.TUTOR, Constants.TUTOR_DASHBOARD);

    private final String displayName;
    private final String dashboardDescription;

    Rol(String displayName, String dashboardDescription) {
        this.displayName = displayName;
        this.dashboardDescription = dashboardDescription;
    }

    public String getDisplayName() {
        return displayName;
    }

    public String getDashboardDescription() {
        return dashboardDescription;
    }

    private static class Constants {
        public static final String ADMIN = "Administrador";
        public static final String ADMIN_DASHBOARD = "Panel Administrador";
        public static final String STUDENT = "Estudiante";
        public static final String STUDENT_DASHBOARD = "Panel Estudiante";
        public static final String TUTOR = "Tutor";
        public static final String TUTOR_DASHBOARD = "Panel Tutor";
    }
}
