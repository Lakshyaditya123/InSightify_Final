import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth';
import { CurrUser } from '../../services/api-interfaces';

@Component({
  selector: 'app-user-profile',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './user-profile.html',
  styleUrls: ['./user-profile.css']
})
export class UserProfile implements OnInit {
  @Output() closeProfile = new EventEmitter<void>();
  currentUser: CurrUser | null = null;
  isClosing = false; // New state to control the slide-out animation
  profile_role=""
  profile=""
  change_navigation=""
  isSuperAdmin=false
  constructor(private authService: AuthService, private router: Router) {}

  ngOnInit() {
    this.currentUser = this.authService.getCurrentUser();
    this.profile_role=this.currentUser?.user_role[0] || ""
    if(this.profile_role==="Super Admin")this.isSuperAdmin=true;
    if(this.router.url.includes('/admin') && this.isSuperAdmin) {
      this.profile="User"
      this.change_navigation='/homescreen'
    }
    else if (this.router.url.includes('/homescreen') && this.isSuperAdmin){
      this.profile="Admin"
      this.change_navigation='/admin'
    }
  }

  // This function starts the closing animation.
  startClose() {
    this.isClosing = true;
    // We wait 300ms (the duration of the animation) before emitting the close event.
    setTimeout(() => {
      this.closeProfile.emit();
    }, 300);
  }

  logout() {
    this.authService.clearUser();
    this.router.navigate(['/login']); 
    this.startClose(); // Use the new animated close method.
  }

  switchProfile() {
    if(this.isSuperAdmin) {
      this.router.navigate([this.change_navigation]); 
    }
    this.startClose();
  }

  onBackdropClick() {
    this.startClose();
  }

  // Prevents clicks inside the panel from triggering the backdrop click.
  onPanelClick(event: Event) {
    event.stopPropagation();
  }
}
