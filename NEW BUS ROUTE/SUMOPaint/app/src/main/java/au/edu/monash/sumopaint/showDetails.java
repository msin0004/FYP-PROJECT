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


public class showDetails extends AppCompatActivity implements View.OnClickListener {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_show_details);

        Button back = (Button) findViewById(R.id.back);
        back.setOnClickListener(showDetails.this);
    }

    @Override
    public void onClick(View v) { // Parameter v stands for the view that was clicked.
        if (v.getId() == R.id.back) {
            finish();
        }
    }


}