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

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.net.UnknownHostException;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    // Declare the UI elements.
    private Button call;
    private Button red;
    private Button orange;
    private Button yellow;
    private Button green;
    private Button blue;
    private Button purple;
    private Button hang_up;

    private Socket clientSocket = null;
    private BufferedWriter out = null;
    private BufferedReader in = null;
    private Boolean ping = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // The only layout for this application is activity_main.xml.

        // Initialise the UI components.
        call = (Button) findViewById(R.id.buttonHelloSUMO);
        red = (Button) findViewById(R.id.buttonRed);
        orange = (Button) findViewById(R.id.buttonOrange);
        yellow = (Button) findViewById(R.id.buttonYellow);
        green = (Button) findViewById(R.id.buttonGreen);
        blue = (Button) findViewById(R.id.buttonBlue);
        purple = (Button) findViewById(R.id.buttonPurple);
        hang_up = (Button) findViewById(R.id.buttonGoodbyeSUMO);

        // Set the listeners so that the buttons can be used for event handling.
        call.setOnClickListener(this);
        red.setOnClickListener(this);
        orange.setOnClickListener(this);
        yellow.setOnClickListener(this);
        green.setOnClickListener(this);
        blue.setOnClickListener(this);
        purple.setOnClickListener(this);
        hang_up.setOnClickListener(this);
    }

    // onClick is called when a view has been clicked.
    @Override
    public void onClick(View v) { // Parameter v stands for the view that was clicked.
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
        } else if(v.getId() == R.id.buttonPurple) {
            new PaintPurple().execute();
        } else if(v.getId() == R.id.buttonGoodbyeSUMO) {
            new DisconnectTask().execute();
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
    private class PaintRed extends AsyncTask<Void, Void, Void> {
        protected Void doInBackground(Void... params) {
            if (ping == true) {
                try {
                    out.write("red");
                    out.flush();
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
            return null;
        }
        protected void onPostExecute(Void... result) {
        }
    }

    // Called to perform work in a worker thread.
    private class PaintOrange extends AsyncTask<Void, Void, Void> {
        protected Void doInBackground(Void... params) {
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
        protected void onPostExecute(Void... result) {
        }
    }

    // Called to perform work in a worker thread.
    private class PaintYellow extends AsyncTask<Void, Void, Void> {
        protected Void doInBackground(Void... params) {
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
        protected void onPostExecute(Void... result) {
        }
    }

    // Called to perform work in a worker thread.
    private class PaintGreen extends AsyncTask<Void, Void, Void> {
        protected Void doInBackground(Void... params) {
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
        protected void onPostExecute(Void... result) {
        }
    }

    // Called to perform work in a worker thread.
    private class PaintBlue extends AsyncTask<Void, Void, Void> {
        protected Void doInBackground(Void... params) {
            if (ping == true) {
                try {
                    out.write("blue");
                    out.flush();
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
            return null;
        }
        protected void onPostExecute(Void... result) {
        }
    }

    // Called to perform work in a worker thread.
    private class PaintPurple extends AsyncTask<Void, Void, Void> {
        protected Void doInBackground(Void... params) {
            if (ping == true) {
                try {
                    out.write("purple");
                    out.flush();
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
            return null;
        }
        protected void onPostExecute(Void... result) {
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
}
