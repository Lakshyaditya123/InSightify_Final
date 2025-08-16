import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth';
import { ApiResponse, CurrUser, securityQues } from '../../services/api-interfaces';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';

@Component({
  selector: 'app-auth-page',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, MatSnackBarModule],
  templateUrl: './auth-page.html',
  styleUrls: ['./auth-page.css']
})
export class AuthPage implements OnInit {
  loginForm: FormGroup;
  signupForm: FormGroup;
  forgotPasswordForm: FormGroup;
  isSignup = false;
  isForgotPassword = false;

  // Properties to track password visibility
  showLoginPassword = false;
  showSignupPassword = false;
  showConfirmPassword = false;
  showNewPassword = false;
  showConfirmNewPassword = false;
  
  securityQuesList: securityQues[] = [];

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private authService: AuthService,
    private snackBar: MatSnackBar
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
      role: ['User', Validators.required]
    });

    this.signupForm = this.fb.group({
      name: ['', Validators.required],
      mobile: ['', [Validators.required, Validators.pattern('^[0-9]{10}$')]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', Validators.required]
    });

    this.forgotPasswordForm = this.fb.group({
        email: ['', [Validators.required, Validators.email]],
        security_question_id: [null, Validators.required],
        security_answer: ['', Validators.required],
        new_password: ['', [Validators.required, Validators.minLength(6)]],
        confirm_new_password: ['', Validators.required]
    });
  }

  ngOnInit() {
    this.authService.clearUser();
    this.getSecurityQuestions();
  }

  getSecurityQuestions() {
      this.authService.getSecQuestions().subscribe({
          next: (res: ApiResponse) => {
              if(res.errCode === 0 && res.data) {
                  this.securityQuesList = res.data;
              } else {
                  this.showError('Could not load security questions.');
              }
          },
          error: (err) => this.showError('Failed to fetch security questions.')
      });
  }

  togglePasswordVisibility(field: 'login' | 'signup' | 'confirm' | 'new' | 'confirmNew') {
    if (field === 'login') this.showLoginPassword = !this.showLoginPassword;
    else if (field === 'signup') this.showSignupPassword = !this.showSignupPassword;
    else if (field === 'confirm') this.showConfirmPassword = !this.showConfirmPassword;
    else if (field === 'new') this.showNewPassword = !this.showNewPassword;
    else if (field === 'confirmNew') this.showConfirmNewPassword = !this.showConfirmNewPassword;
  }

  toggleMode(event: Event): void {
    event.preventDefault();
    this.isSignup = !this.isSignup;
    this.loginForm.reset({ role: 'User' });
    this.signupForm.reset();
  }

  toggleForgotPassword(event: Event): void {
      event.preventDefault();
      this.isForgotPassword = !this.isForgotPassword;
      this.forgotPasswordForm.reset();
  }

  signup() {
    if (this.signupForm.valid) {
      if (this.signupForm.value.password !== this.signupForm.value.confirmPassword) {
        this.showError('Passwords do not match.');
        return;
      }
      const { confirmPassword, ...payload } = this.signupForm.value;

      this.authService.signup(payload).subscribe({
        next: (res: ApiResponse) => {
          if (res.errCode === 0) {
            this.showSuccess('Signup successful! Please login.');
            this.isSignup = false;
          } else {
            this.showError(res.message || 'Signup failed.');
          }
        },
        error: (err) => this.showError('An error occurred during signup.')
      });
    }
  }

  login() {
    if (this.loginForm.valid) {
      const payload = this.loginForm.value;
      this.authService.login(payload).subscribe({
        next: (res: ApiResponse) => {
          if (res.errCode === 0 && res.datarec) {
            this.showSuccess('Login successful!');
            const user: CurrUser = res.datarec;
            this.authService.setUser(user);

            if (payload.role === 'Admin' || payload.role === "Super Admin") {
              this.router.navigate(['/admin']);
            } else {
              this.router.navigate(['/homescreen']);
            }
          } else {
            this.showError(res.message || 'Login failed. Please check your credentials.');
          }
        },
        error: (err) => this.showError('An error occurred during login.')
      });
    }
  }

    forgotPassword() {
      if(this.forgotPasswordForm.valid) {
          if (this.forgotPasswordForm.value.new_password !== this.forgotPasswordForm.value.confirm_new_password) {
              this.showError('New passwords do not match.');
              return;
          }

          const formValue = { ...this.forgotPasswordForm.value };
          formValue.security_question_id = parseInt(formValue.security_question_id, 10);
          delete formValue.confirm_new_password;
          
          this.authService.forgetPasswd(formValue).subscribe({
              next: (res: ApiResponse) => {
                  if (res.errCode === 0) {
                      this.showSuccess('Password has been reset successfully! Please login.');
                      this.isForgotPassword = false;
                  } else {
                      this.showError(res.message || 'Password reset failed.');
                  }
              },
              error: (err) => this.showError('An error occurred during password reset.')
          });
      }
  }

  showSuccess(message: string) {
    this.snackBar.open(message, 'Close', {
      duration: 3000,
      panelClass: ['snack-success'],
    });
  }

  showError(message: string) {
    this.snackBar.open(message, 'Close', {
      duration: 3000,
      panelClass: ['snack-error'],
    });
  }
}
