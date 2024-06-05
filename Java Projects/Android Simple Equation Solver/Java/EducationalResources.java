package com.example.mathapp;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

public class EducationalResources extends AppCompatActivity {

    private View linearEquationsSection;
    private View quadraticEquationsSection;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_educational_resources);

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        linearEquationsSection = findViewById(R.id.linear_equations_section);
        quadraticEquationsSection = findViewById(R.id.quadratic_equations_section);

        Button buttonLinear = findViewById(R.id.button_linear);
        Button buttonQuadratic = findViewById(R.id.button_quadratic);

        buttonLinear.setOnClickListener(v -> showSection(R.id.linear_equations_section));
        buttonQuadratic.setOnClickListener(v -> showSection(R.id.quadratic_equations_section));

        showSection(R.id.linear_equations_section);
    }

    private void showSection(int sectionId) {
        linearEquationsSection.setVisibility(sectionId == R.id.linear_equations_section ? View.VISIBLE : View.GONE);
        quadraticEquationsSection.setVisibility(sectionId == R.id.quadratic_equations_section ? View.VISIBLE : View.GONE);
    }

    @Override
    public void onBackPressed() {
        super.onBackPressed();
        overridePendingTransition(R.anim.slide_in_left, R.anim.slide_out_right);
    }
}
