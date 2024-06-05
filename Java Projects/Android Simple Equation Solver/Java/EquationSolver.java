package com.example.mathapp;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

public class EquationSolver extends AppCompatActivity {

    private View linearEquationsSection;
    private View quadraticEquationsSection;
    private TextView textViewSolutionLinear;
    private TextView textViewStepsLinear;
    private TextView textViewSolutionQuadratic;
    private TextView textViewStepsQuadratic;
    private View viewDividerLinear;
    private View viewDividerQuadratic;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_equation_solver);

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        linearEquationsSection = findViewById(R.id.linear_equations_section);
        quadraticEquationsSection = findViewById(R.id.quadratic_equations_section);

        textViewSolutionLinear = findViewById(R.id.textview_solution_linear);
        textViewStepsLinear = findViewById(R.id.textview_steps_linear);
        textViewSolutionQuadratic = findViewById(R.id.textview_solution_quadratic);
        textViewStepsQuadratic = findViewById(R.id.textview_steps_quadratic);
        viewDividerLinear = findViewById(R.id.view_divider_linear);
        viewDividerQuadratic = findViewById(R.id.view_divider_quadratic);

        Button buttonLinear = findViewById(R.id.button_linear);
        Button buttonQuadratic = findViewById(R.id.button_quadratic);
        Button buttonCalculateLinear = findViewById(R.id.button_calculate_linear);
        Button buttonCalculateQuadratic = findViewById(R.id.button_calculate_quadratic);

        buttonLinear.setOnClickListener(v -> showSection(R.id.linear_equations_section));
        buttonQuadratic.setOnClickListener(v -> showSection(R.id.quadratic_equations_section));
        buttonCalculateLinear.setOnClickListener(v -> calculateLinearEquation());
        buttonCalculateQuadratic.setOnClickListener(v -> calculateQuadraticEquation());

        showSection(R.id.linear_equations_section);
    }

    private void showSection(int sectionId) {
        linearEquationsSection.setVisibility(sectionId == R.id.linear_equations_section ? View.VISIBLE : View.GONE);
        quadraticEquationsSection.setVisibility(sectionId == R.id.quadratic_equations_section ? View.VISIBLE : View.GONE);
    }

    private void calculateLinearEquation() {
        EditText editTextA = findViewById(R.id.edittext_a);
        EditText editTextB = findViewById(R.id.edittext_b);
        EditText editTextResult = findViewById(R.id.edittext_result);

        try {
            double a = Double.parseDouble(editTextA.getText().toString());
            double b = Double.parseDouble(editTextB.getText().toString());
            double result = Double.parseDouble(editTextResult.getText().toString());

            if (a == 0) {
                if (b == result) {
                    textViewSolutionLinear.setText("Solution: The value of x can be that of any real number.");
                    textViewStepsLinear.setText("Step 1: 0x + " + b + " = " + result + "\n" +
                            "Step 2: " + b + " = " + result + "\n" +
                            "Step 3: Since " + b + " = " + result + " , x can be any real number.");
                } else {
                    textViewSolutionLinear.setText("Solution: The function has no real solutions.");
                    textViewStepsLinear.setText("Step 1: 0x + " + b + " = " + result + "\n" +
                            "Step 2: " + b + " != " + result + "\n" +
                            "Step 3: Since " + b + " != " + result + " , there are no real solutions.");
                }
            } else {
                double x = (result - b) / a;
                String solutionText = "Solution: x = " + x;
                textViewSolutionLinear.setText(solutionText);

                String stepsText = "Step 1: " + a + "x + " + b + " = " + result + "\n" +
                        "Step 2: " + a + "x = " + (result - b) + "\n" +
                        "Step 3: x = (" + result + " - " + b + ") / " + a + "\n" +
                        "Step 4: x = " + x;
                textViewStepsLinear.setText(stepsText);
            }

            textViewSolutionLinear.setVisibility(View.VISIBLE);
            textViewStepsLinear.setVisibility(View.VISIBLE);
            viewDividerLinear.setVisibility(View.VISIBLE);
        } catch (NumberFormatException e) {
            Toast.makeText(this, "Please enter valid numbers", Toast.LENGTH_LONG).show();
        }
    }


    private void calculateQuadraticEquation() {
        EditText editTextQuadA = findViewById(R.id.edittext_quad_a);
        EditText editTextQuadB = findViewById(R.id.edittext_quad_b);
        EditText editTextQuadC = findViewById(R.id.edittext_quad_c);
        EditText editTextQuadResult = findViewById(R.id.edittext_quad_result);

        try {
            double a = Double.parseDouble(editTextQuadA.getText().toString());
            double b = Double.parseDouble(editTextQuadB.getText().toString());
            double c = Double.parseDouble(editTextQuadC.getText().toString());
            double result = Double.parseDouble(editTextQuadResult.getText().toString());

            if (a == 0) {
                if (b == 0) {
                    if (c == result) {
                        textViewSolutionQuadratic.setText("Solution: The value of x can that of be any real number.");
                        textViewStepsQuadratic.setText("Step 1: 0x^2 + 0x + " + c + " = " + result + "\n" +
                                "Step 2: " + c + " = " + result + "\n" +
                                "Step 3: Since " + c + " = " + result + ", x can be any real number.");
                    } else {
                        textViewSolutionQuadratic.setText("Solution: The function has no real solutions.");
                        textViewStepsQuadratic.setText("Step 1: 0x^2 + 0x + " + c + " = " + result + "\n" +
                                "Step 2: " + c + " != " + result + "\n" +
                                "Step 3: Since " + c + " != " + result + ", there are no real solutions.");
                    }
                } else {
                    double x = (result - c) / b;
                    String solutionText = "Solution: x = " + x;
                    textViewSolutionQuadratic.setText(solutionText);

                    String stepsText = "Step 1: 0x^2 + " + b + "x + " + c + " = " + result + "\n" +
                            "Step 2: " + b + "x = " + (result - c) + "\n" +
                            "Step 3: x = (" + result + " - " + c + ") / " + b + "\n" +
                            "Step 4: x = " + x;
                    textViewStepsQuadratic.setText(stepsText);
                }
            } else {
                double discriminant = b * b - 4 * a * (c - result);

                if (discriminant > 0) {
                    double x1 = (-b + Math.sqrt(discriminant)) / (2 * a);
                    double x2 = (-b - Math.sqrt(discriminant)) / (2 * a);
                    String solutionText = "Solution: x1 = " + x1 + ", x2 = " + x2;
                    textViewSolutionQuadratic.setText(solutionText);

                    String stepsText = "Step 1: " + a + "x^2 + " + b + "x + " + c + " = " + result + "\n" +
                            "Step 2: " + a + "x^2 + " + b + "x + " + (c - result) + " = 0\n" +
                            "Step 3: Discriminant = " + b + "^2 - 4 * " + a + " * " + (c - result) + "\n" +
                            "Step 4: Discriminant = " + discriminant + "\n" +
                            "Step 5: x1 = (" + -b + " + sqrt(" + discriminant + ")) / (2 * " + a + ")\n" +
                            "Step 6: x2 = (" + -b + " - sqrt(" + discriminant + ")) / (2 * " + a + ")\n" +
                            "Step 7: x1 = " + x1 + "\n" +
                            "Step 8: x2 = " + x2;
                    textViewStepsQuadratic.setText(stepsText);
                } else if (discriminant == 0) {
                    double x = -b / (2 * a);
                    String solutionText = "Solution: x1 = x2 = " + x;
                    textViewSolutionQuadratic.setText(solutionText);

                    String stepsText = "Step 1: " + a + "x^2 + " + b + "x + " + c + " = " + result + "\n" +
                            "Step 2: " + a + "x^2 + " + b + "x + " + (c - result) + " = 0\n" +
                            "Step 3: Discriminant = " + b + "^2 - 4 * " + a + " * " + (c - result) + "\n" +
                            "Step 4: Discriminant = " + discriminant + "\n" +
                            "Step 5: The discriminant is 0 so we have x1 = x2 = (" + -b + ") / (2 * " + a + ")\n" +
                            "Step 6: x1 = x2 = " + x;
                    textViewStepsQuadratic.setText(stepsText);
                } else {
                    textViewSolutionQuadratic.setText("There are no real solutions.");
                    String stepsText = "Step 1: " + a + "x^2 + " + b + "x + " + c + " = " + result + "\n" +
                            "Step 2: " + a + "x^2 + " + b + "x + " + (c - result) + " = 0\n" +
                            "Step 3: Discriminant = " + b + "^2 - 4 * " + a + " * " + (c - result) + "\n" +
                            "Step 4: Discriminant = " + discriminant + "\n" +
                            "Step 5: Since the discriminant is < 0, there are no real solutions.";
                    textViewStepsQuadratic.setText(stepsText);
                }
            }

            textViewSolutionQuadratic.setVisibility(View.VISIBLE);
            textViewStepsQuadratic.setVisibility(View.VISIBLE);
            viewDividerQuadratic.setVisibility(View.VISIBLE);
        } catch (NumberFormatException e) {
            Toast.makeText(this, "Please enter valid numbers", Toast.LENGTH_LONG).show();
        }
    }



    @Override
    public void onBackPressed() {
        super.onBackPressed();
        overridePendingTransition(R.anim.slide_in_left, R.anim.slide_out_right);
    }
}
