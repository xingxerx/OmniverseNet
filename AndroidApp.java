 java
import android.os.Bundle;
import android.app.Activity;
public class MindPortalApp extends Activity {
 MindPortalInterface mpi;
 protected void onCreate(Bundle savedInstanceState) {
  super.onCreate(savedInstanceState);
  mpi = new MindPortalInterface();
 }
}

