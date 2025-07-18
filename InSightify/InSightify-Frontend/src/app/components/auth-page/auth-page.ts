import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth';
import { ApiResponse, CurrUser } from '../../services/api-interfaces';

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
  isSignup = false;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private authService: AuthService
  ) {

    // this.authService.clearUser();

    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required]
    });

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

  signup() {
    if (this.signupForm.valid) {
      let payload: any = this.signupForm.value;
      delete payload['confirmPassword'];

      this.authService.signup(payload).subscribe((res: ApiResponse) => {
        if (res.errCode == 0) {
          alert('Signup Successfully');
          this.isSignup = false;
        } else {
          alert('Signup Failed!');
          this.isSignup = true;
        }
      });
    }
  }

  login() {
    if (this.loginForm.valid) {
      let payload: any = this.loginForm.value;
      this.authService.login(payload).subscribe((res: ApiResponse) => {
        if (res.errCode == 0) {
          alert('Login Successfully');
          const user: CurrUser = res.datarec;
          this.authService.setUser(user);
          this.router.navigate(['/homescreen']);
        } else {
          alert('Login Failed!');
        }
      });
    }
  }
}