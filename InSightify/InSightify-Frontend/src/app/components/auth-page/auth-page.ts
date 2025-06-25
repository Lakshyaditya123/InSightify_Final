import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-auth-page',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './auth-page.html',
  styleUrls: ['./auth-page.css']
})
export class AuthPage {
  loginForm: FormGroup;
  signupForm: FormGroup;
  isSignup = false; // 🔁 Controls which form is shown

  constructor(private fb: FormBuilder, private router: Router) {
    // 🧾 Login Form
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required]
    });

    // 🧾 Signup Form
    this.signupForm = this.fb.group({
      name: ['', Validators.required],
      mobile: ['', [Validators.required, Validators.minLength(10)]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', Validators.required]
    });
  }

  toggleMode(event: Event): void {
    event.preventDefault();
    this.isSignup = !this.isSignup;
    this.loginForm.reset();
    this.signupForm.reset();
  }

  onSubmit(): void {
    if (this.isSignup) {
      // 🔐 SIGNUP logic
      const { name, mobile, email, password, confirmPassword } = this.signupForm.value;

      if (!this.signupForm.valid) {
        alert('Please fill out all fields properly.');
        return;
      }

      if (password !== confirmPassword) {
        alert('Passwords do not match!');
        return;
      }

      console.log('Sign Up with:', name, email, mobile);
      this.toggleMode(new Event('click')); // Redirects to login view
    } else {
      // 🔓 LOGIN logic
      const { email, password } = this.loginForm.value;

      if (!this.loginForm.valid) {
        alert('Please enter valid credentials.');
        return;
      }

      console.log('Login with:', email);
      this.router.navigate(['/homescreen']); // 🔁 Redirect to homescreen
    }
  }
}
