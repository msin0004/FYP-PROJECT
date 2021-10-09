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
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.SpinnerAdapter;
import android.widget.SpinnerAdapter;
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
    private TextView test_input1;
    private TextView server_connection;
    private String var_testing = null;

    private Socket clientSocket = null;
    private BufferedWriter out = null;
    private BufferedReader in = null;
    private Boolean ping = false;
    private String incoming = null;
    //private int inflag = 0;
    private Timer listenTimer;
    private Handler handler;
    private String[] stops = new String[]{"Stop 1", "Stop 2", "Stop 3", "Stop 4", "Stop 5", "Stop 6", "Stop 7", "practise"};
    private String[] busses = new String[]{"Bus 1", "Bus 2", "Bus 3"};
    private String stop = null; //stop value to get data on
    private String bus_decision = null;
    private String get = "receive"; //variable that requests data from server to be sent
    private String send = null; //variable that stores data being sent to server
    //private Spinner spinner;

    //flags
    private int flag_connection = 0;
    private String instruction = null;

    //variables from server to print on device
    private String ETA = "ETA";
    private String Pass = "Passengers onboard";
    private String Seats = "Seats available";
    private String ETA_val = null;
    private String Pass_val = null;
    private String Seats_val = null;
    private String Bus1 = "BUS 1";
    private String Bus2 = "BUS 2";
    private String Bus3 = "BUS 3";
    //private String bus_no = null;

    //loop to initialise the bus information
    private Integer bus_no = 0;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // The only layout for this application is activity_main.xml.

        // Initialise the UI components.
        Button call = (Button) findViewById(R.id.buttonHelloSUMO);
        /*
        Button red = (Button) findViewById(R.id.buttonRed);
        Button orange = (Button) findViewById(R.id.buttonOrange);
        Button yellow = (Button) findViewById(R.id.buttonYellow);
        Button green = (Button) findViewById(R.id.buttonGreen);
        Button blue = (Button) findViewById(R.id.buttonBlue);
        */
        Button refresh = (Button) findViewById(R.id.refresh);
       // Button hang_up = (Button) findViewById(R.id.buttonGoodbyeSUMO);
        Button go_button = (Button) findViewById(R.id.buttongo);
        Button send = (Button) findViewById(R.id.buttonsend);
        Spinner spinner = (Spinner)findViewById(R.id.spinners);
       Spinner bus_option = (Spinner)findViewById(R.id.select_bus);

        //sample code
        //NOTE
        //need to define these on the postexecute part of a click otherview the app will crash with an error
        //test_input = (TextView) findViewById(R.id.textinput);
        //server_connection = (TextView) findViewById(R.id.server_connection);
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(MainActivity.this,
                android.R.layout.simple_spinner_item,stops);
        spinner.setAdapter(adapter);
        ArrayAdapter<String> adapter_1 = new ArrayAdapter<String>(MainActivity.this,
                android.R.layout.simple_spinner_item,busses);
        bus_option.setAdapter(adapter_1);

        // Set the listeners so that the buttons can be used for event handling.
        call.setOnClickListener(this);
        /*
        red.setOnClickListener(this);
        orange.setOnClickListener(this);
        yellow.setOnClickListener(this);
        green.setOnClickListener(this);
        blue.setOnClickListener(this);
         */
        refresh.setOnClickListener(this);
        //hang_up.setOnClickListener(this);
        go_button.setOnClickListener(this);
        //spinner.setOnItemSelectedListener(this);

        handler = new Handler();
    }

    // onClick is called when a view has been clicked.
    @Override
    public void onClick(View v) { // Parameter v stands for the view that was clicked.
        final Handler handler = new Handler();



        if(v.getId() == R.id.buttonHelloSUMO) { // getId() returns the view's identifier
            if(ping == false)
            {
                new ConnectTask().execute();
            }
            else if(ping == true)
            {
                flag_connection = 0;
                new DisconnectTask().execute();
            }

        }
        /*else if(v.getId() == R.id.buttonRed) {
            new PaintRed().execute();
        } else if(v.getId() == R.id.buttonOrange) {
            new PaintOrange().execute();
        } else if(v.getId() == R.id.buttongo) {
            new Getdata().execute();
        } else if(v.getId() == R.id.buttonGreen) {
            new PaintGreen().execute();
        } else if(v.getId() == R.id.buttonBlue) {
            new PaintBlue().execute();
            //new page button

        }*/

        else if(v.getId() == R.id.buttongo)
        {
            //get value from spinner
            Spinner spinner = (Spinner)findViewById(R.id.spinners);
            stop = spinner.getSelectedItem().toString();  //STORE STOP VALUE SELECTED INTO STOP VARIABLE
            new Getdata().execute();
        }
        else if(v.getId() == R.id.buttonsend)
        {
            Spinner bus_option = (Spinner)findViewById(R.id.select_bus);
            bus_decision = bus_option.getSelectedItem().toString();
        }


        else if(v.getId() == R.id.refresh) {

            //incoming = null;


            new Refresh().execute();
            //final Handler handler = new Handler();
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
        }

    }


    private class ListenTask extends AsyncTask<Boolean, Void, String> {
        protected String doInBackground(Boolean... params) {
            if (ping == true) {
                try {
                    Log.i("listen","before the incoming");
                    if(in.ready()) {
                        Log.i("ready","inside ready");
                        incoming = String.valueOf(in.readLine());
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
            //test_input = (TextView) findViewById(R.id.textinput);
            //test_input.setText(result);

            if(instruction == "bus_no")
            {

                TextView testing = (TextView) findViewById(R.id.businput1_empty);
                testing.setText(result);

                bus_no = Integer.parseInt(incoming);
                TextView bus1_name = (TextView) findViewById(R.id.businput1_name);
                TextView bus1_eta = (TextView) findViewById(R.id.businput1_ETA);
                TextView bus1_pass = (TextView) findViewById(R.id.businput1_Occupancy);
                TextView bus1_seat = (TextView) findViewById(R.id.businput1_Seats);
                TextView bus2_name = (TextView) findViewById(R.id.businput2_name);
                TextView bus2_eta = (TextView) findViewById(R.id.businput2_ETA);
                TextView bus2_pass = (TextView) findViewById(R.id.businput2_Occupancy);
                TextView bus2_seat = (TextView) findViewById(R.id.businput2_Seats);
                TextView bus3_name = (TextView) findViewById(R.id.businput3_name);
                TextView bus3_eta = (TextView) findViewById(R.id.businput3_ETA);
                TextView bus3_pass = (TextView) findViewById(R.id.businput3_Occupancy);
                TextView bus3_seat = (TextView) findViewById(R.id.businput3_Seats);

                if(bus_no == 0)
                {
                    bus1_name.setText("");
                    bus1_eta.setText("");
                    bus1_pass.setText("");
                    bus1_seat.setText("");
                    bus2_name.setText("");
                    bus2_eta.setText("");
                    bus2_pass.setText("");
                    bus2_seat.setText("");
                    bus3_name.setText("");
                    bus3_eta.setText("");
                    bus3_pass.setText("");
                    bus3_seat.setText("");
                }

               if(bus_no == 1)
               {
                   testing.setText(result);
                   bus1_name.setText(Bus1);
                   bus1_eta.setText(ETA);
                   bus1_pass.setText(Pass);
                   bus1_seat.setText(Seats);
                   bus2_name.setText("");
                   bus2_eta.setText("");
                   bus2_pass.setText("");
                   bus2_seat.setText("");
                   bus3_name.setText("");
                   bus3_eta.setText("");
                   bus3_pass.setText("");
                   bus3_seat.setText("");

               }
               if(bus_no == 2)
               {
                   bus1_name.setText(Bus1);
                   bus1_eta.setText(ETA);
                   bus1_pass.setText(Pass);
                   bus1_seat.setText(Seats);
                   bus2_name.setText(Bus2);
                   bus2_eta.setText(ETA);
                   bus2_pass.setText(Pass);
                   bus2_seat.setText(Seats);
                   bus3_name.setText("");
                   bus3_eta.setText("");
                   bus3_pass.setText("");
                   bus3_seat.setText("");
               }
               if(bus_no == 3)
               {
                   bus1_name.setText(Bus1);
                   bus1_eta.setText(ETA);
                   bus1_pass.setText(Pass);
                   bus1_seat.setText(Seats);
                   bus2_name.setText(Bus2);
                   bus2_eta.setText(ETA);
                   bus2_pass.setText(Pass);
                   bus2_seat.setText(Seats);
                   bus3_name.setText(Bus3);
                   bus3_eta.setText(ETA);
                   bus3_pass.setText(Pass);
                   bus3_seat.setText(Seats);
               }
            }






        }
    }




    // Called to perform work in a worker thread.
    // Calls SUMO.
    private class ConnectTask extends AsyncTask<Void, Void, Boolean> {
        protected Boolean doInBackground(Void... params) {
            if (ping == false) {
                try {
                    clientSocket = new Socket("10.0.2.2", 8080);
                    out = new BufferedWriter(new OutputStreamWriter(clientSocket.getOutputStream()));
                    in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                    ping = true;
                    flag_connection = 1;
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
            //added functionality to view connection status of the device to the server
           server_connection = (TextView) findViewById(R.id.server_connect);
           Button connect = (Button) findViewById(R.id.buttonHelloSUMO);
           if(flag_connection == 1)
           {
               server_connection.setText("Connected");
               connect.setText("Close Server");
           }
           flag_connection = 1;
        }
    }

    // Called to perform work in a worker thread.
    private class Getdata extends AsyncTask<Void, Void, String> {
        protected String doInBackground(Void... params) {
            if (ping == true) {
                try {
                    //checking if stop is null
                    if(stop != null) {
                        send = stop;
                        out.write(send);
                        out.flush();

                        //sleep so the server has time to read and perform tasks for the previous write command
                        try
                        {
                            Thread.sleep(  1000 );
                        }
                        catch ( InterruptedException e )
                        {
                            e.printStackTrace();
                        }

                        //request server for data relating to previous write command
                        out.write("bus_no");
                        out.flush();
                        instruction = "bus_no";
                    }

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
            Log.i("red", "post listen");

            return incoming;
        }
        protected void onPostExecute(Boolean result) {
          //  test_input = (TextView) findViewById(R.id.businput1_name);
          //  test_input.setText(stop);

        }
    }

    // Called to perform work in a worker thread.
    private class Refresh extends AsyncTask<Void, Void, String> {
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
            test_input = (TextView) findViewById(R.id.businput1_name);
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
            //change status and button option
            server_connection = (TextView) findViewById(R.id.server_connect);
            server_connection.setText("Not Connected");
            Button connect = (Button) findViewById(R.id.buttonHelloSUMO);
            connect.setText("Connect to Server");
        }
    }


    // Called to perform work in a worker thread.
    private class PaintRed extends AsyncTask<Void, Void, String> {
        protected String doInBackground(Void... params) {
            if (ping == true) {
                try {
                    out.write("stop7");
                    out.flush();
                    Log.i("red", "post stop7");
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
                    Log.i("red", "post send");
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
            Log.i("red", "post listen");

            return incoming;
        }
        protected void onPostExecute(String result) {
            Log.i("red", "post execute");
            test_input = (TextView) findViewById(R.id.businput1_name);
            test_input.setText(result);
            TextView testing = (TextView) findViewById(R.id.businput1_empty);
            testing.setText(var_testing);
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
            test_input = (TextView) findViewById(R.id.businput1_name);
            test_input.setText("TESTING OF orange BUTTON");
            TextView editing = (TextView) findViewById(R.id.server_connect);
            editing.setText("EDITED FROM orange BUTTON INPUT");
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
            test_input = (TextView) findViewById(R.id.businput1_name);
            test_input.setText("TESTING OF green BUTTON");
            TextView editing = (TextView) findViewById(R.id.businput1_empty);
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

}
