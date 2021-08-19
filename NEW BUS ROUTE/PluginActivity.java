/**
 *  Program:  SumoEmbed SAS Giovanni
 *            - a plug-in for "Torque Pro" by Ian Hawkins
 *            - controls a set of vehicles so that they all achieve the same average speed, without having to reveal private information about their speed to their neighbours
 *  Author:   Wynita Griggs
 *  Date:     20th May, 2016
 */

package ie.ucd.smarttransport.sumoembedsasgiovanni;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.text.NumberFormat;
import java.util.Timer;
import java.util.TimerTask;

import org.prowl.torque.remote.ITorqueService;

import android.app.Activity;
import android.content.ComponentName;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.os.IBinder;
import android.os.RemoteException;
import android.util.Log;
import android.view.View;
import android.view.Menu;
import android.widget.Button;
import android.widget.TextView;

public class PluginActivity extends Activity implements View.OnClickListener {

    private ITorqueService torqueService;

    // private static final int TILT_Y_PID = 0xff124b;
    private static final int SPEED_PID = 0x0d; ///// OBD Speed /////

    // Declare the UI elements.
    private Button call;
    private TextView current_speed;
    private TextView advised_speed;
    private Button hang_up;

    private Socket clientSocket = null;
    private BufferedWriter out = null;
    private BufferedReader in = null;
    private Boolean ping = false;
    private String incoming;
    private Timer listenTimer;

    private NumberFormat nf;

    private Handler handler;
    private Timer updateTimer;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_plugin); // The only layout for this application is activity_main.xml.

        // Initialise the UI components.
        call = (Button) findViewById(R.id.button_1);
        current_speed = (TextView) findViewById(R.id.textView_2);
        advised_speed = (TextView) findViewById(R.id.textView_4);
        hang_up = (Button) findViewById(R.id.button_2);

        // Set the listeners so that the buttons can be used for event handling.
        call.setOnClickListener(this);
        hang_up.setOnClickListener(this);

        // Set a maximum of 0 decimal places for vehicle readings.
        nf = NumberFormat.getInstance();
        nf.setMaximumFractionDigits(0);

        handler = new Handler();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_plugin, menu);
        return true;
    }

    @Override
    protected void onResume() {
        super.onResume();

        // Bind to the torque service.
        Intent intent = new Intent();
        intent.setClassName("org.prowl.torque", "org.prowl.torque.remote.TorqueService");
        boolean successfulBind = bindService(intent, connection, 0);

        if (successfulBind) {
            updateTimer = new Timer();
            updateTimer.schedule(new TimerTask() { public void run() {
                update();
            }}, 1000, 1000);
        }
    }

    @Override
    protected void onPause() {
        super.onPause();
        updateTimer.cancel();
        unbindService(connection);
    }

    // Do an update.
    public void update() {
        String current_speed_text = "";

        try {
            // float value = Math.abs(torqueService.getValueForPid(TILT_Y_PID, true));
            float value = torqueService.getValueForPid(SPEED_PID, true); ///// OBD Speed /////

            current_speed_text = nf.format(value);
        } catch(RemoteException e) {
            Log.e(getClass().getCanonicalName(), e.getMessage(), e);
        }

        if (ping == true) {
            try {
                out.write(current_speed_text);
                out.flush();
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }

        // Update the widget.
        final String myText_speed = current_speed_text;
        handler.post(new Runnable() {
            public void run() {
                current_speed.setText(myText_speed);
            }
        });
    }

    // onClick is called when a view has been clicked.
    @Override
    public void onClick(View v) { // Parameter v stands for the view that was clicked.
        if(v.getId() == R.id.button_1) { // getId() returns the view's identifier

            new ConnectTask().execute();

            final Handler handler = new Handler();
            listenTimer = new Timer();
            incoming = null;

            TimerTask doAsynchronousTask = new TimerTask() {
                @Override
                public void run() {
                    handler.post(new Runnable() {
                        public void run() {
                            try {
                                ListenTask performBackgroundTask = new ListenTask();
                                performBackgroundTask.execute(ping);
                            } catch (Exception e) {
                                // TODO Auto-generated catch block
                            }
                        }
                    });
                }
            };
            listenTimer.schedule(doAsynchronousTask, 100, 1000);

        } else if(v.getId() == R.id.button_2) {
            new DisconnectTask().execute();
        }
    }

    // Called to perform work in a worker thread.
    // Calls SUMO.
    private class ConnectTask extends AsyncTask<Void, Void, Boolean> {
        protected Boolean doInBackground(Void... params) {
            if (ping == false) {
                try {
                    // clientSocket = new Socket("137.43.44.98", 50100); ///// WYNITA'S DESKTOP /////
                    clientSocket = new Socket("137.43.44.90", 50200); ///// RODRIGO'S DESKTOP /////
                    out = new BufferedWriter(new OutputStreamWriter(clientSocket.getOutputStream()));
                    in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                    ping = true;
                } catch (UnknownHostException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
            return ping;
        }
        protected void onPostExecute(Boolean result) {
        }
    }

    // Called to perform work in a worker thread.
    // Listens for advise from SUMO.
    private class ListenTask extends AsyncTask<Boolean, Void, String> {
        protected String doInBackground(Boolean... params) {
            if (ping == true) {
                try {
                    incoming = in.readLine();
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            } else if (ping == false) {
                listenTimer.cancel();
                incoming = "No Advice";
            }
            return incoming;
        }
        protected void onPostExecute(String result) {
            advised_speed.setText(result);
        }
    }

    // Called to perform work in a worker thread.
    // Disconnects from SUMO.
    private class DisconnectTask extends AsyncTask<Void, Void, Boolean> {
        protected Boolean doInBackground(Void... params) {
            if (ping == true) {
                try {
                    ping = false;
                    out.write("quit");
                    out.close(); // close the writer connected to the socket
                    in.close(); // close the reader connected to the socket
                    clientSocket.close(); // close the socket
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
            return ping;
        }
        protected void onPostExecute(Boolean result) {
        }
    }

    /**
     * Bits of service code. You usually won't need to change this.
     */

    private ServiceConnection connection = new ServiceConnection() {
        public void onServiceConnected(ComponentName arg0, IBinder service) {
            torqueService = ITorqueService.Stub.asInterface(service);
        };
        public void onServiceDisconnected(ComponentName name) {
            torqueService = null;
        };
    };

}