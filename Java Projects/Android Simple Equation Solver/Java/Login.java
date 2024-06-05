package com.example.mathapp;

import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;

public class Login extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        findViewById(R.id.buttonLoginToggle).setOnClickListener(v -> showLoginFragment());
        findViewById(R.id.buttonRegisterToggle).setOnClickListener(v -> showRegisterFragment());

        if (savedInstanceState == null) {
            showLoginFragment();
        }
    }

    void showLoginFragment() {
        replaceFragment(new LoginFragment());
    }

    void showRegisterFragment() {
        replaceFragment(new RegisterFragment());
    }

    private void replaceFragment(Fragment fragment) {
        getSupportFragmentManager().beginTransaction()
                .replace(R.id.fragment_container, fragment)
                .commit();
    }
}
