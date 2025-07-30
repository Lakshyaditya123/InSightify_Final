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
  profile="User"
  constructor(private authService: AuthService, private router: Router) {}

  ngOnInit() {
    this.currentUser = this.authService.getCurrentUser();
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
    this.router.navigate(['/homescreen']); 
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
