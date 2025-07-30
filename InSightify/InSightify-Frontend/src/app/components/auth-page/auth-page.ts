// import { Component, OnInit } from '@angular/core';
// import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
// import { CommonModule } from '@angular/common';
// import { Router } from '@angular/router';
// import { AuthService } from '../../services/auth';
// import { ApiResponse, CurrUser } from '../../services/api-interfaces';
// import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
// import { timeout } from 'rxjs';

// @Component({
//   selector: 'app-auth-page',
//   standalone: true,
//   imports: [CommonModule, ReactiveFormsModule,MatSnackBarModule ],
//   templateUrl: './auth-page.html',
//   styleUrls: ['./auth-page.css']
// })
// export class AuthPage {
//   loginForm: FormGroup;
//   signupForm: FormGroup;
//   isSignup = false;
//   loginAsAdmin=false;

//   constructor(
//     private fb: FormBuilder,
//     private router: Router,
//     private authService: AuthService,
//     private snackBar: MatSnackBar
//   ) {
//     this.loginForm = this.fb.group({
//       email: ['', [Validators.required, Validators.email]],
//       password: ['', Validators.required]
//     });

//     this.signupForm = this.fb.group({
//       name: ['', Validators.required],
//       mobile: ['', [Validators.required, Validators.minLength(10)]],
//       email: ['', [Validators.required, Validators.email]],
//       password: ['', [Validators.required, Validators.minLength(6)]],
//       confirmPassword: ['', Validators.required]
//     });
//   }
//    ngOnInit() {
//     this.authService.clearUser();
//   }
//   toggleMode(event: Event): void {
//     event.preventDefault();
//     this.isSignup = !this.isSignup;
//     this.loginForm.reset();
//     this.signupForm.reset();
//   }

//   signup() {
//     if (this.signupForm.valid) {
//       let payload: any = this.signupForm.value;
//       delete payload['confirmPassword'];

//       this.authService.signup(payload).subscribe((res: ApiResponse) => {
//         if (res.errCode == 0) {
//          this.showSuccess();
//           this.isSignup = false;
//         } else {
//          this.showError()
//           this.isSignup = true;
//         }
//       });
//     }
//   }

//   login() {
//     if (this.loginForm.valid) {
//       let payload: any = this.loginForm.value;
//       this.authService.login(payload).subscribe((res: ApiResponse) => {
//         if (res.errCode == 0) {
//           this.showSuccess()
//           const user: CurrUser = res.datarec;
//           this.authService.setUser(user);
//           if (this.loginAsAdmin) this.router.navigate(['/admin']);
//           else this.router.navigate(['/homescreen']);
//         } else {
//           this.showError()
//         }
//       });
//     }
//   }
// showSuccess() {
//   this.snackBar.open('Login successful!', 'Close', {
//     duration: 3000,
//     panelClass: ['snack-success'],
//   });
// }

// showError() {
//   this.snackBar.open('Login failed. Please try again.', 'Close', {
//     duration: 3000,
//     panelClass: ['snack-error'],
//   });
// }

// }

import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth';
import { ApiResponse, CurrUser } from '../../services/api-interfaces';
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
  isSignup = false;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private authService: AuthService,
    private snackBar: MatSnackBar
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
      role: ['user', Validators.required] // Add role control with 'user' as default
    });

    this.signupForm = this.fb.group({
      name: ['', Validators.required],
      mobile: ['', [Validators.required, Validators.pattern('^[0-9]{10}$')]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', Validators.required]
    });
  }

  ngOnInit() {
    this.authService.clearUser();
  }

  toggleMode(event: Event): void {
    event.preventDefault();
    this.isSignup = !this.isSignup;
    this.loginForm.reset({ role: 'user' }); // Reset form but keep default role
    this.signupForm.reset();
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
      const { role, ...payload } = this.loginForm.value;

      this.authService.login(payload).subscribe({
        next: (res: ApiResponse) => {
          if (res.errCode === 0 && res.datarec) {
            this.showSuccess('Login successful!');
            const user: CurrUser = res.datarec;
            this.authService.setUser(user);

            // Navigate based on the selected role
            if (role === 'admin') {
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
