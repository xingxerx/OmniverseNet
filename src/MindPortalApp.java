 java
import android.os.Bundle;
import android.app.Activity;
// It's good practice to import all classes you use directly.
// Assuming MindPortalInterface is in the same package or imported elsewhere.
// import your.package.name.MindPortalInterface;

public class MindPortalApp extends Activity {
    // Consider making fields private unless accessed by subclasses or package members.
    // MindPortalInterface mpi;
    private MindPortalInterface mpi;

    @Override // Good practice to always include @Override annotation
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // It's common to set a layout file here using setContentView()
        // e.g., setContentView(R.layout.activity_main);
        // Without this, your activity will have a blank screen.

        // Initialize the interface
        mpi = new MindPortalInterface();

        // You might want to do something with 'mpi' here,
        // like setting up listeners or calling initialization methods.
    }

    // Consider adding lifecycle methods like onPause(), onResume(), onDestroy()
    // to manage resources associated with mpi if necessary.
    /*
    @Override
    protected void onDestroy() {
        super.onDestroy();
        // Clean up resources if mpi holds any (e.g., close connections, unregister listeners)
        if (mpi != null) {
            // mpi.cleanup(); // Example cleanup method
        }
    }
    */
}

// Assuming MindPortalInterface exists like this (example):
/*
package your.package.name; // Or same package as MindPortalApp

class MindPortalInterface {
    public MindPortalInterface() {
        // Constructor logic
        System.out.println("MindPortalInterface initialized");
    }

    // Add methods needed for the interface
    public void someAction() {
        // Action logic
    }

    public void cleanup() {
        // Resource cleanup logic
    }
}
*/
