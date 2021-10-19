/*
   Program: Bus Stop & Go App
   Goal:    Allows a user to connect to a bus simulation, select a bus and provide feedback on which bus they would take
   Author:  Meher Singh
   Date:    23rd October 2021
 */

package au.edu.monash.sumopaint;

import androidx.appcompat.app.AppCompatActivity;

import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
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
    private TextView test_input;
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
    private String[] stops = new String[]{"Stop 1", "Stop 2", "Stop 3", "Stop 4", "Stop 5", "Stop 6", "Stop 7"};
    private String[] buses = new String[]{"Bus 1", "Bus 2", "Bus 3"};
    private String stop = null; //stop value to get data on
    private String bus_decision = null;
    private String get = "receive"; //variable that requests data from server to be sent
    private String send = null; //variable that stores data being sent to server
    //private Spinner spinner;

    //flags
    private String instruction = null;

    //variables from server to print on device
    private String title_update = null;
    private String Bus1 = "BUS 1";
    private String Bus2 = "BUS 2";
    private String Bus3 = "BUS 3";
    private String Bus1_ETA = null;
    private String Bus1_Pass = null;
    private String Bus1_Seat = null;
    private String Bus2_ETA = null;
    private String Bus2_Pass = null;
    private String Bus2_Seat = null;
    private String Bus3_ETA = null;
    private String Bus3_Pass = null;
    private String Bus3_Seat = null;
    private String Bus1_ETA_val = null;
    private String Bus1_Pass_val = null;
    private String Bus1_Seat_val = null;
    private String Bus2_ETA_val = null;
    private String Bus2_Pass_val = null;
    private String Bus2_Seat_val = null;
    private String Bus3_ETA_val = null;
    private String Bus3_Pass_val = null;
    private String Bus3_Seat_val = null;
    private String user_input = null;       //user input decision

    //loop to initialise the bus information
    private Integer bus_no = 0;
    private Integer receive_counter = 0;
    private Integer receive_max = 9999;        //max amount of data received from server at given time.


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // The only layout for this application is activity_main.xml.

        // Initialise the UI components.
        Button call = (Button) findViewById(R.id.buttonHelloSUMO);
        Button refresh = (Button) findViewById(R.id.refresh);
        Button go_button = (Button) findViewById(R.id.buttongo);
        Button send_button = (Button) findViewById(R.id.buttonsend);
        Spinner spinner = (Spinner) findViewById(R.id.spinners);
        Spinner bus_option = (Spinner) findViewById(R.id.select_bus);

        //sample code
        //NOTE
        //need to define these on the postexecute part of a click otherview the app will crash with an error
        //test_input = (TextView) findViewById(R.id.textinput);
        //server_connection = (TextView) findViewById(R.id.server_connection);
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(MainActivity.this,
                android.R.layout.simple_spinner_item, stops);
        spinner.setAdapter(adapter);
        ArrayAdapter<String> adapter_1 = new ArrayAdapter<String>(MainActivity.this,
                android.R.layout.simple_spinner_item, buses);
        bus_option.setAdapter(adapter_1);

        // Set the listeners so that the buttons can be used for event handling.
        //these buttons are the only way to perform tasks in the app
        call.setOnClickListener(this);
        refresh.setOnClickListener(this);
        go_button.setOnClickListener(this);
        send_button.setOnClickListener(this);

        handler = new Handler();
    }

    // onClick is called when a view has been clicked.
    @Override
    public void onClick(View v) { // Parameter v stands for the view that was clicked.
        final Handler handler = new Handler();


        if (v.getId() == R.id.buttonHelloSUMO) { // getId() returns the view's identifier
            if (ping == false) {
                new ConnectTask().execute();
            } else if (ping == true) {
                new DisconnectTask().execute();
            }

        } else if (v.getId() == R.id.buttongo) {
            //get value from spinner
            Spinner spinner = (Spinner) findViewById(R.id.spinners);
            stop = spinner.getSelectedItem().toString();  //STORE STOP VALUE SELECTED INTO STOP VARIABLE
            //run the process to get data
            new Getdata().execute();
        } else if (v.getId() == R.id.buttonsend) {
            //get value from spinner (for bus decision)
            Spinner bus_option = (Spinner) findViewById(R.id.select_bus);
            bus_decision = bus_option.getSelectedItem().toString();
            //get user input value
            EditText text_input = (EditText) findViewById(R.id.text_input);
            user_input = text_input.getText().toString();
            text_input.getText().clear();
            //run the process
            new Senddata().execute();

        } else if (v.getId() == R.id.refresh) {
            new Getdata().execute();
        }

    }


    private class ListenTask extends AsyncTask<Boolean, Void, String> {
        protected String doInBackground(Boolean... params) {
            Log.i("listen", "background");
            if (ping == true) {
                try {
                    //Log.i("listen","before the incoming");
                    if (in.ready()) {
                        //Log.i("ready","inside ready");
                        incoming = String.valueOf(in.readLine());
                        if (incoming != null) {
                            //Log.i("if null","not null ");
                        } else {
                            //Log.i("if null"," is null ");
                            return incoming;
                        }
                    }
                    //this currently doesnt work
                    //NEED TO REMOVE LATER
                    if (incoming == "finished") {
                        Log.i("listen", "ending");
                        listenTimer.cancel(); //cancel listening
                    }
                    // listenTimer.cancel();
                    //Log.i("listen","afeter the incoming");
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            } else if (ping == false) {
                //Log.i("listen","before the incoming");
                listenTimer.cancel();
                incoming = "ping = false";
            }
            return incoming;
        }

        protected void onPostExecute(String result) {
            Log.i("listen", "post  incoming");
            Log.i("incoming", incoming);
            //Log.i("listen", "result");
            Log.i("result", result);


            //declaring all text positions
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
            TextView bus1_eta_value = (TextView) findViewById(R.id.businput1_ETAvalue);
            TextView bus1_pass_value = (TextView) findViewById(R.id.businput1_Occupancyvalue);
            TextView bus1_seat_value = (TextView) findViewById(R.id.businput1_Seatsvalue);
            TextView bus2_eta_value = (TextView) findViewById(R.id.businput2_ETAvalue);
            TextView bus2_pass_value = (TextView) findViewById(R.id.businput2_Occupancyvalue);
            TextView bus2_seat_value = (TextView) findViewById(R.id.businput2_Seatsvalue);
            TextView bus3_eta_value = (TextView) findViewById(R.id.businput3_ETAvalue);
            TextView bus3_pass_value = (TextView) findViewById(R.id.businput3_Occupancyvalue);
            TextView bus3_seat_value = (TextView) findViewById(R.id.businput3_Seatsvalue);
            TextView title = (TextView) findViewById(R.id.title);

            //get number of buses arriving to stop
            if (instruction == "bus_no") {
                //testing value
                //TextView testing = (TextView) findViewById(R.id.businput1_empty);
                //testing.setText(result);

                bus_no = Integer.parseInt(incoming);

                //calculate the maximum amount of data that can be sent
                //equals 3 information per bus
                receive_max = bus_no * 3;
                receive_counter = 0;

                //reset all values
                bus1_name.setText("LOADING");
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
                bus1_eta_value.setText("");
                bus1_pass_value.setText("");
                bus1_seat_value.setText("");
                bus2_eta_value.setText("");
                bus2_pass_value.setText("");
                bus2_seat_value.setText("");
                bus3_eta_value.setText("");
                bus3_pass_value.setText("");
                bus3_seat_value.setText("");

                //comparing bus numbers
                if (bus_no == 0) {
                    //setting to no buses arriving
                    Bus1 = "No buses are arriving to this stop";
                    title_update = "Select Stop and click go";
                    /*
                    bus1_name.setText("No buses are arriving to this stop");
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
                    */
                }

                if (bus_no == 1) {
                    Bus1 = "BUS 1";
                    Bus1_ETA = "ETA (minutes)";
                    Bus1_Pass = "Passengers onboard";
                    Bus1_Seat = "Seats taken";
                    Bus2 = null;
                    Bus2_ETA = null;
                    Bus2_Pass = null;
                    Bus2_Seat = null;
                    Bus3 = null;
                    Bus3_ETA = null;
                    Bus3_Pass = null;
                    Bus3_Seat = null;
                    title_update = "Select bus and enter decision";
                }
                if (bus_no == 2) {
                    Bus1 = "BUS 1";
                    Bus1_ETA = "ETA (minutes)";
                    Bus1_Pass = "Passengers onboard";
                    Bus1_Seat = "Seats taken";
                    Bus2 = "BUS 2";
                    Bus2_ETA = "ETA (minutes)";
                    Bus2_Pass = "Passengers onboard";
                    Bus2_Seat = "Seats taken";
                    Bus3 = null;
                    Bus3_ETA = null;
                    Bus3_Pass = null;
                    Bus3_Seat = null;
                    title_update = "Select bus and enter decision";
                }
                if (bus_no == 3) {
                    Bus1 = "BUS 1";
                    Bus1_ETA = "ETA (minutes)";
                    Bus1_Pass = "Passengers onboard";
                    Bus1_Seat = "Seats taken";
                    Bus2 = "BUS 2";
                    Bus2_ETA = "ETA (minutes)";
                    Bus2_Pass = "Passengers onboard";
                    Bus2_Seat = "Seats taken";
                    Bus3 = "BUS 3";
                    Bus3_ETA = "ETA (minutes)";
                    Bus3_Pass = "Passengers onboard";
                    Bus3_Seat = "Seats taken";
                    title_update = "Select bus and enter decision";
                }
                instruction = "bus_no1";
            }
            //get all the data from the server
            else if (instruction == "bus_no1") {

                //checking if max number is received
                if (receive_counter.equals(receive_max)) {
                    //reset all counters
                    instruction = "";
                    receive_counter = 0;
                    //cancel the listening because all the information has been received
                    listenTimer.cancel();

                    //print all the bus information gathered
                    bus1_name.setText(Bus1);
                    bus1_eta.setText(Bus1_ETA);
                    bus1_pass.setText(Bus1_Pass);
                    bus1_seat.setText(Bus1_Seat);
                    bus2_name.setText(Bus2);
                    bus2_eta.setText(Bus2_ETA);
                    bus2_pass.setText(Bus2_Pass);
                    bus2_seat.setText(Bus2_Seat);
                    bus3_name.setText(Bus3);
                    bus3_eta.setText(Bus3_ETA);
                    bus3_pass.setText(Bus3_Pass);
                    bus3_seat.setText(Bus3_Seat);
                    bus1_eta_value.setText(Bus1_ETA_val);
                    bus1_pass_value.setText(Bus1_Pass_val);
                    bus1_seat_value.setText(Bus1_Seat_val);
                    bus2_eta_value.setText(Bus2_ETA_val);
                    bus2_pass_value.setText(Bus2_Pass_val);
                    bus2_seat_value.setText(Bus2_Seat_val);
                    bus3_eta_value.setText(Bus3_ETA_val);
                    bus3_pass_value.setText(Bus3_Pass_val);
                    bus3_seat_value.setText(Bus3_Seat_val);
                    title.setText(title_update);

                    //reset all the bus information
                    Bus1_ETA_val = null;
                    Bus1_Pass_val = null;
                    Bus1_Seat_val = null;
                    Bus2_ETA_val = null;
                    Bus2_Pass_val = null;
                    Bus2_Seat_val = null;
                    Bus3_ETA_val = null;
                    Bus3_Pass_val = null;
                    Bus3_Seat_val = null;
                    Bus1 = null;
                    Bus1_ETA = null;
                    Bus1_Pass = null;
                    Bus1_Seat = null;
                    Bus2 = null;
                    Bus2_ETA = null;
                    Bus2_Pass = null;
                    Bus2_Seat = null;
                    Bus3 = null;
                    Bus3_ETA = null;
                    Bus3_Pass = null;
                    Bus3_Seat = null;
                }
                //bus 1 eta
                else if (receive_counter == 0) {
                    //bus1_eta_value.setText(result);
                    Bus1_ETA_val = result;
                    receive_counter++;
                }
                //bus 1 pass
                else if (receive_counter == 1) {
                    //bus1_pass_value.setText(result);
                    Bus1_Pass_val = result;
                    receive_counter++;
                }
                //bus 1 seat
                else if (receive_counter == 2) {
                    //bus1_seat_value.setText(result);
                    Bus1_Seat_val = result;
                    receive_counter++;
                }
                //bus 2 eta
                else if (receive_counter == 3) {
                    // bus2_eta_value.setText(result);
                    Bus2_ETA_val = result;
                    receive_counter++;
                }
                //bus 2 pass
                else if (receive_counter == 4) {
                    // bus2_pass_value.setText(result);
                    Bus2_Pass_val = result;
                    receive_counter++;
                }
                //bus 2 seat
                else if (receive_counter == 5) {
                    // bus2_seat_value.setText(result);
                    Bus2_Seat_val = result;
                    receive_counter++;
                }
                //bus 3 eta
                else if (receive_counter == 6) {
                    //bus3_eta_value.setText(result);
                    Bus3_ETA_val = result;
                    receive_counter++;
                }
                //bus 3 pass
                else if (receive_counter == 7) {
                    //bus3_pass_value.setText(result);
                    Bus3_Pass_val = result;
                    receive_counter++;
                }
                //bus 3seat
                else if (receive_counter == 8) {
                    //bus3_seat_value.setText(result);
                    Bus3_Seat_val = result;
                    receive_counter++;
                }


            }

            //after sending data to the user
            else if (instruction == "send_data") {
                title.setText("Thanks for your input :) !");
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
                bus1_eta_value.setText("");
                bus1_pass_value.setText("");
                bus1_seat_value.setText("");
                bus2_eta_value.setText("");
                bus2_pass_value.setText("");
                bus2_seat_value.setText("");
                bus3_eta_value.setText("");
                bus3_pass_value.setText("");
                bus3_seat_value.setText("");
                listenTimer.cancel();
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
                    Log.i("before", "before print");
                    //server_connection.setText("testing");
                    Log.i("test", "text");

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
            TextView title = (TextView) findViewById(R.id.title);
            //reset bus1 name (refers to clearing the sent message)
            TextView bus1_name = (TextView) findViewById(R.id.businput1_name);
            if (ping == true) {
                server_connection.setText("Connected");
                connect.setText("Close Server");
                title.setText("Select Stop and click go");
                bus1_name.setText("");
            }


        }
    }

    // Called to perform work in a worker thread.
    private class Getdata extends AsyncTask<Void, Void, String> {
        protected String doInBackground(Void... params) {
            if (ping == true) {
                try {
                    //checking if stop is null
                    if (stop != null) {
                        send = stop;
                        out.write(send);
                        out.flush();

                        //sleep so the server has time to read and perform tasks for the previous write command
                        try {
                            Thread.sleep(1000);
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }

                        //request server for data relating to previous write command
                        out.write("bus_no");
                        out.flush();
                        // set instruction value
                        instruction = "bus_no";
                    }

                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }


                //LISTEN CODE
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
            Log.i("getdata", "post listen");
            return incoming;
        }

        protected void onPostExecute(Boolean result) {
            Log.i("getdata", "post execute code");

        }
    }

    //Called to perform work in a worker thread
    private class Senddata extends AsyncTask<Void, Void, String> {
        protected String doInBackground(Void... params) {
            if (ping == true) {
                try {

                    if (user_input != null) {
                        //send
                        out.write(bus_decision);
                        out.flush();

                        //sleep so the server has time to read and perform tasks for the previous write command
                        try {
                            Thread.sleep(1000);
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }

                        //request server for data relating to previous write command

                        out.write(user_input);
                        out.flush();
                        // set instruction value
                        instruction = "send_data";
                    }

                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }


                //LISTEN CODE
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
            Log.i("senddata", "post listen");
            return incoming;
        }

        protected void onPostExecute(Boolean result) {
            Log.i("senddata", "post execute code");

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
            TextView title = (TextView) findViewById(R.id.title);
            title.setText("Connect to server");

            //declaring bus information text view
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

            //declaring value text views
            TextView bus1_eta_value = (TextView) findViewById(R.id.businput1_ETAvalue);
            TextView bus1_pass_value = (TextView) findViewById(R.id.businput1_Occupancyvalue);
            TextView bus1_seat_value = (TextView) findViewById(R.id.businput1_Seatsvalue);
            TextView bus2_eta_value = (TextView) findViewById(R.id.businput2_ETAvalue);
            TextView bus2_pass_value = (TextView) findViewById(R.id.businput2_Occupancyvalue);
            TextView bus2_seat_value = (TextView) findViewById(R.id.businput2_Seatsvalue);
            TextView bus3_eta_value = (TextView) findViewById(R.id.businput3_ETAvalue);
            TextView bus3_pass_value = (TextView) findViewById(R.id.businput3_Occupancyvalue);
            TextView bus3_seat_value = (TextView) findViewById(R.id.businput3_Seatsvalue);

            //declaring edit views
            EditText text_input = (EditText) findViewById(R.id.text_input);

            //clearing values
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
            bus1_eta_value.setText("");
            bus1_pass_value.setText("");
            bus1_seat_value.setText("");
            bus2_eta_value.setText("");
            bus2_pass_value.setText("");
            bus2_seat_value.setText("");
            bus3_eta_value.setText("");
            bus3_pass_value.setText("");
            bus3_seat_value.setText("");
            text_input.getText().clear();

        }
    }

}//end of Main Activity


