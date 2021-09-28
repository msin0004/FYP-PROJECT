/*
   Program: SUMOPaint - Version 3.0
   Goal:    Allows one to change the colour of a vehicle in SUMO on-the-fly.
   Author:  Wynita Griggs
   Date:    15th October, 2019
 */

package au.edu.monash.sumopaint;

import androidx.appcompat.app.AppCompatActivity;

import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import android.util.Log;
import android.os.Handler;
import java.util.Timer;
import java.util.TimerTask;
import android.content.Intent;


public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    // Declare the UI elements.
    //private Button call;
   // private Button red;
   // private Button orange;
   // private Button green;
   // private Button purple;
   // private Button hang_up;
    private TextView test_input;
    private TextView server_connection;

    private Socket clientSocket = null;
    private BufferedWriter out = null;
    private BufferedReader in = null;
    private Boolean ping = false;
    private String incoming = null;
    //private int inflag = 0;
    private Timer listenTimer;
    private Handler handler;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // The only layout for this application is activity_main.xml.

        // Initialise the UI components.
        Button call = (Button) findViewById(R.id.buttonHelloSUMO);
        Button red = (Button) findViewById(R.id.buttonRed);
        Button orange = (Button) findViewById(R.id.buttonOrange);
        Button yellow = (Button) findViewById(R.id.buttonYellow);
        Button green = (Button) findViewById(R.id.buttonGreen);
        Button blue = (Button) findViewById(R.id.buttonBlue);
        Button purple = (Button) findViewById(R.id.buttonPurple);
        Button hang_up = (Button) findViewById(R.id.buttonGoodbyeSUMO);

        //sample code
        //NOTE
        //need to define these on the postexecute part of a click otherview the app will crash with an error
        //test_input = (TextView) findViewById(R.id.textinput);
        //server_connection = (TextView) findViewById(R.id.server_connection);


        // Set the listeners so that the buttons can be used for event handling.
        call.setOnClickListener(this);
        red.setOnClickListener(this);
        orange.setOnClickListener(this);
        yellow.setOnClickListener(this);
        green.setOnClickListener(this);
        blue.setOnClickListener(this);
        purple.setOnClickListener(this);
        hang_up.setOnClickListener(this);

        handler = new Handler();
    }

    // onClick is called when a view has been clicked.
    @Override
    public void onClick(View v) { // Parameter v stands for the view that was clicked.
        final Handler handler = new Handler();
        if(v.getId() == R.id.buttonHelloSUMO) { // getId() returns the view's identifier
            new ConnectTask().execute();

        } else if(v.getId() == R.id.buttonRed) {
            new PaintRed().execute();
        } else if(v.getId() == R.id.buttonOrange) {
            new PaintOrange().execute();
        } else if(v.getId() == R.id.buttonYellow) {
            new PaintYellow().execute();
        } else if(v.getId() == R.id.buttonGreen) {
            new PaintGreen().execute();
        } else if(v.getId() == R.id.buttonBlue) {
            new PaintBlue().execute();
            //new page button
        } else if(v.getId() == R.id.buttonPurple) {

            //incoming = null;


            new PaintPurple().execute();

        } else if(v.getId() == R.id.buttonGoodbyeSUMO) {
            new DisconnectTask().execute();
        }
    }


    private class ListenTask extends AsyncTask<Boolean, Void, String> {
        protected String doInBackground(Boolean... params) {
            if (ping == true) {
                try {
                    Log.i("listen","before the incoming");
                    if(in.ready()) {
                        Log.i("ready","inside ready");
                        incoming = in.readLine();
                        if (incoming != null) {
                            Log.i("if null","not null ");
                        } else {
                            Log.i("if null"," is null ");
                            return incoming;
                        }
                    }
                    listenTimer.cancel(); //cancel listening
                    Log.i("listen","afeter the incoming");
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            } else if (ping == false) {
                Log.i("listen","before the incoming");
                listenTimer.cancel();
                incoming = "ping = false";
            }
            return incoming;
        }
        protected void onPostExecute(String result) {
            Log.i("listen", "post execute");
            test_input = (TextView) findViewById(R.id.textinput);
            test_input.setText(result);
        }
    }




    // Called to perform work in a worker thread.
    // Calls SUMO.
    private class ConnectTask extends AsyncTask<Void, Void, Boolean> {
        int flag_connection = 1;
        protected Boolean doInBackground(Void... params) {
            if (ping == false) {
                try {
                    clientSocket = new Socket("10.0.2.2", 8080);
                    out = new BufferedWriter(new OutputStreamWriter(clientSocket.getOutputStream()));
                    in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                    ping = true;
                    flag_connection = 2;
                    Log.i("before", "before print");
                    //server_connection.setText("testing");
                    Log.i("test","text");

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
           server_connection = (TextView) findViewById(R.id.server_connect);
           if(flag_connection == 2)
           {
               server_connection.setText("Connected");
           }
           else
           {
               server_connection.setText("Not Connected");
           }
           flag_connection =1;
        }
    }

    // Called to perform work in a worker thread.
    private class PaintRed extends AsyncTask<Void, Void, String> {
        protected String doInBackground(Void... params) {
            if (ping == true) {
                try {
                    out.write("stop7");
                    out.flush();
                    try
                    {
                        Thread.sleep(  1000 );
                    }
                    catch ( InterruptedException e )
                    {
                        e.printStackTrace();
                    }

                    out.write("send");
                    out.flush();
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }

            listenTimer = new Timer();
            //incoming = null; //set the incoming to null before receiving new data

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
            return incoming;
        }
        protected void onPostExecute(String result) {
            test_input = (TextView) findViewById(R.id.textinput);
            test_input.setText(result);
        }
    }

    // Called to perform work in a worker thread.
    private class PaintOrange extends AsyncTask<Void, Void, Boolean> {
        protected Boolean doInBackground(Void... params) {
            if (ping == true) {
                try {
                    out.write("orange");
                    out.flush();
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
            return null;
        }
        protected void onPostExecute(Boolean result) {
            test_input = (TextView) findViewById(R.id.textinput);
            test_input.setText("TESTING OF orange BUTTON");
            TextView editing = (TextView) findViewById(R.id.server_connect);
            editing.setText("EDITED FROM orange BUTTON INPUT");
        }
    }

    // Called to perform work in a worker thread.
    private class PaintYellow extends AsyncTask<Void, Void, Boolean> {
        protected Boolean doInBackground(Void... params) {
            if (ping == true) {
                try {
                    out.write("yellow");
                    out.flush();
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
            return null;
        }
        protected void onPostExecute(Boolean result) {

        }
    }

    // Called to perform work in a worker thread.
    private class PaintGreen extends AsyncTask<Void, Void, Boolean> {
        protected Boolean doInBackground(Void... params) {
            if (ping == true) {
                try {
                    out.write("green");
                    out.flush();
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
            return null;
        }
        protected void onPostExecute(Boolean result) {
            test_input = (TextView) findViewById(R.id.textinput);
            test_input.setText("TESTING OF green BUTTON");
            TextView editing = (TextView) findViewById(R.id.server_connection);
            editing.setText("EDITED FROM green BUTTON INPUT");
        }
    }

    // Called to perform work in a worker thread.
    private class PaintBlue extends AsyncTask<Void, Void, Boolean> {
        protected Boolean doInBackground(Void... params) {

            return null;
        }
        protected void onPostExecute(Boolean result) {
            Intent intent = new Intent(MainActivity.this, showDetails.class);
            startActivity(intent);
        }
    }

    // Called to perform work in a worker thread.
    private class PaintPurple extends AsyncTask<Void, Void, String> {
       // String message = "";
        //char[] buffer1 = new char[2048];
       // int test = 0;

        protected String doInBackground(Void... params) {
            //Ping means connection to server
            if (ping) {
                try {
                    Log.i("before", "updating");
                    out.write("update");
                    out.flush();
                    Log.i("after", "updating");
                    //test_input.setText("testing");

                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
                /*
                    Log.i("before", "reading");
                    //message = in.readLine();

                    Log.i("after", "reading");
                    //test_input.setText(test);
                    Log.i("output", String.valueOf(test));
                    /*

                    SO in.read provides a integer input from the

                    */

                listenTimer = new Timer();
                //incoming = null; //set the incoming to null before receiving new data

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


            }
            return incoming;
        }
        protected void onPostExecute(String result) {
            //test_input.setText("testing");
           // test_input = (TextView) findViewById(R.id.textinput);
           // test_input.setText("TESTING OF UPDATE BUTTON");
           // TextView editing = (TextView) findViewById(R.id.server_connection);
           // editing.setText("EDITED FROM Update BUTTON INPUT");
           // char[] buffer = new char[2048];
           // String message = "";
/*          try{
                //message = String.valueOf(in.read(buffer));
                //message = in.readLine();
                //message = in.readUTF();
               // test_input.setText(message);
            }catch(IOException e){
                e.printStackTrace();
            }

*/
            /*
            try {
                Log.i("before", "reading");
                //message = in.readLine();
                //test = in.read(buffer1, 0, 2048);
               // test = in.read(buffer1, 0, 2048);
                Log.i("after", "reading");
                Log.i("after_test", String.valueOf(buffer1));
                message = String.valueOf(buffer1);
                //test_input.setText(message);
            } catch (IOException e) {
                e.printStackTrace();
            }
*/

            //test_input.setText(test);

            //forever loop until
            //Log.i("update", "post execute");
            //while(incoming == null) {
           // }
            //Log.i("update", "after forever loop");
            test_input = (TextView) findViewById(R.id.textinput);
            test_input.setText(result);
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
            server_connection = (TextView) findViewById(R.id.server_connect);
            server_connection.setText("Not Connected");
        }
    }
}
