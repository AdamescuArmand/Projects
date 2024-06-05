package com.example.mathapp;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.Toast;
import androidx.fragment.app.Fragment;

public class RegisterFragment extends Fragment {

    private DatabaseHelper dbHelper;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_register, container, false);

        dbHelper = new DatabaseHelper(getActivity());

        view.findViewById(R.id.buttonRegister).setOnClickListener(v -> registerUser(view));

        return view;
    }

    private void registerUser(View view) {
        EditText editTextNewUsername = view.findViewById(R.id.editTextNewUsername);
        EditText editTextNewPassword = view.findViewById(R.id.editTextNewPassword);

        String newUsername = editTextNewUsername.getText().toString().trim();
        String newPassword = editTextNewPassword.getText().toString().trim();

        if (newUsername.isEmpty() || newPassword.isEmpty()) {
            Toast.makeText(getActivity(), "Please enter new username and password", Toast.LENGTH_SHORT).show();
            return;
        }

        if (newPassword.length() < 5) {
            Toast.makeText(getActivity(), "Password must be at least 5 characters long", Toast.LENGTH_SHORT).show();
            return;
        }

        boolean usernameExists = dbHelper.checkUsernameExists(newUsername);
        if (usernameExists) {
            Toast.makeText(getActivity(), "Username already exists", Toast.LENGTH_SHORT).show();
            return;
        }

        long result = dbHelper.insertUser(newUsername, newPassword);
        if (result != -1) {
            Toast.makeText(getActivity(), "Registration successful", Toast.LENGTH_SHORT).show();
            ((Login) getActivity()).showLoginFragment();
        } else {
            Toast.makeText(getActivity(), "Registration failed", Toast.LENGTH_SHORT).show();
        }
    }
}
