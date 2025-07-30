import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { CurrUser } from '../../services/api-interfaces';
import { AuthService } from '../../services/auth';
@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css'
})
export class Navbar implements OnInit {
  constructor(private authService: AuthService, private router: Router) {}
  ngOnInit() {
    const currentUser: CurrUser | null = this.authService.getCurrentUser();
  }
  
  show_profile:boolean=false;
  navigateToProfile(){
    this.show_profile=!this.show_profile;
  }

  navigateToHome() {
    this.authService.clearUser()
    this.router.navigate(['/login']);
  }
}
