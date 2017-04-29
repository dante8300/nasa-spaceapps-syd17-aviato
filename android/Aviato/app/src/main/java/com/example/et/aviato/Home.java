package com.example.et.aviato;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentActivity;
import android.util.Log;
import android.view.KeyEvent;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
import android.widget.TextView;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by et on 030 30 Apr.
 */


class GetUrlContentTask extends AsyncTask<String, Integer, String> {
    private Home home;

    public GetUrlContentTask(Home home) {
        this.home = home;
    }

    protected String doInBackground(String... urls) {
        URL url = null;
        try {
            url = new URL(urls[0]);
        } catch (MalformedURLException e) {
            e.printStackTrace();
        }
        HttpURLConnection connection = null;
        try {
            connection = (HttpURLConnection) url.openConnection();
        } catch (IOException e) {
            e.printStackTrace();
        }
        try {
            connection.setRequestMethod("GET");
        } catch (ProtocolException e) {
            e.printStackTrace();
        }
        connection.setDoOutput(true);
        connection.setConnectTimeout(5000);
        connection.setReadTimeout(5000);
        try {
            connection.connect();
            Log.v("NET", "WE ARE HERE");
        } catch (IOException e) {
            e.printStackTrace();
        }
        BufferedReader rd = null;
        try {
            rd = new BufferedReader(new InputStreamReader(connection.getInputStream()));
        } catch (IOException e) {
            e.printStackTrace();
        }
        String content = "", line;
        try {
            while ((line = rd.readLine()) != null) {
                content += line + "\n";
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return content;
    }

    protected void onProgressUpdate(Integer... progress) {
    }

    protected void onPostExecute(String result) {
        home.displayMessage(result);
    }
}

public class Home extends FragmentActivity implements OnMapReadyCallback, View.OnKeyListener {

    private GoogleMap mMap;
    private List<JSONObject> sightingPoints = new ArrayList<>();
    private int curSighting = 0;
    private Marker curMarker = null;
    private TextView textView = null;

    public void displayMessage(String message) {
        AlertDialog alertDialog = new AlertDialog.Builder(Home.this).create();
        alertDialog.setTitle("Bird status");
        alertDialog.setMessage(message);
        alertDialog.setButton(AlertDialog.BUTTON_NEUTRAL, "OK",
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                    }
                });
        alertDialog.show();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.home);

        //Get Data From Text Resource File Contains Json Data.
        InputStream inputStream = getResources().openRawResource(R.raw.sighting_points);
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();

        int ctr;
        try {
            ctr = inputStream.read();
            while (ctr != -1) {
                byteArrayOutputStream.write(ctr);
                ctr = inputStream.read();
            }
            inputStream.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        Log.v("Sightings Data:", byteArrayOutputStream.toString());
        try {
            JSONArray jArray = new JSONArray(
                    byteArrayOutputStream.toString());
            ArrayList<String[]> data = new ArrayList<String[]>();
            for (int i = 0; i < jArray.length(); i++) {
                sightingPoints.add(jArray.getJSONObject(i));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        AutoCompleteTextView textView = (AutoCompleteTextView) findViewById(R.id.birdSearch);
        String[] birds = getResources().getStringArray(R.array.birds_array);
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, birds);
        textView.setAdapter(adapter);
        textView.setOnKeyListener(this);
        this.textView = textView;

        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.discoverMap);
        mapFragment.getMapAsync(this);

        Button snapButton = (Button) findViewById(R.id.cameraButton);
        snapButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                curSighting = (curSighting + 1) % sightingPoints.size();
                JSONObject posObj = sightingPoints.get(curSighting);
                try {
                    setMarker(posObj.getDouble("latitude"), posObj.getDouble("longitude"));
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });
    }

    public void setMarker(double lat, double lng) {
        LatLng pos = new LatLng(lat, lng);
        if (curMarker != null) {
            curMarker.remove();
        }
        curMarker = mMap.addMarker(new MarkerOptions().position(pos).title("You are here"));
        mMap.moveCamera(CameraUpdateFactory.newLatLng(pos));
    }

    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;
        JSONObject posObj = sightingPoints.get(curSighting);
        try {
            setMarker(posObj.getDouble("latitude"), posObj.getDouble("longitude"));
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    @Override
    public boolean onKey(View view, int keyCode, KeyEvent keyEvent) {
        Log.v("APP", "SEARCHED!!!");
            //if (textView.getText().equals("Blacktailed Godwit")) {
                textView.setText("");
                new GetUrlContentTask(this).execute("http://eternalthinker.co");
                return true;
            //}
        //return false;
    }
}
