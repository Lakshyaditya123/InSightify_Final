import { Component, OnInit, Output, EventEmitter, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth';
import { ApiResponse, CurrUser } from '../../services/api-interfaces';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { ImageUrlPipe } from '../../pipes/image-pipe'; // Import the new pipe

@Component({
  selector: 'app-user-profile',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule,ImageUrlPipe],
  templateUrl: './user-profile.html',
  styleUrls: ['./user-profile.css']
})
export class UserProfile implements OnInit {
  @Output() closeProfile = new EventEmitter<void>();
  @Input() userIdToDisplay: number | null = null; 

  currentUser: CurrUser | null = null;
  displayUser: CurrUser | null = null;
  
  isClosing = false;
  isSuperAdmin = false;
  isEditMode = false;
  profileForm: FormGroup;
  selectedProfilePic: File | null = null;

  constructor(
    private authService: AuthService, 
    private router: Router,
    private fb: FormBuilder
  ) {
   this.profileForm = this.fb.group({
    bio: [this.displayUser?.user_bio || '']
  });
  }

 currentModeLabel = '';

ngOnInit() {
  this.currentUser = this.authService.getCurrentUser();
  this.isSuperAdmin = this.currentUser?.user_role.includes('Super Admin') ?? false;

  this.currentModeLabel = this.router.url.includes('/admin') ? 'User' : 'Admin';
  
  const targetUserId = this.userIdToDisplay ?? this.currentUser?.user_id;
  if (targetUserId) {
    this.loadUserProfile(targetUserId);
  }
}

  loadUserProfile(userId: number) {
    this.authService.get_user_profile({ user_id: userId }).subscribe({
      next: (res: ApiResponse) => {
        if (res.errCode === 0 && res.datarec) {
          this.displayUser = res.datarec;
          if (this.currentUser && this.displayUser?.user_id === this.currentUser.user_id) {
            this.profileForm.patchValue({
              bio: this.displayUser.user_bio
            });
          }
        } else {
          console.error("Failed to load profile:", res.message);
        }
      },
      error: (err) => console.error("API error loading profile:", err)
    });
  }

  toggleEditMode() {
    this.isEditMode = !this.isEditMode;
    if (this.isEditMode && this.displayUser) {
      this.profileForm.patchValue({
        bio: this.displayUser.user_bio
      });
    }
  }

  onProfilePicSelected(event: any) {
  const file: File = event.target.files[0];
  if (file && file.type === 'image/png') {
    this.selectedProfilePic = file;
  } else {
    alert("Only PNG files are allowed.");
  }
}
  saveProfile() {
    if (!this.profileForm.valid || !this.currentUser) return;

   const formData = new FormData();
    formData.append('user_id', String(this.currentUser.user_id));    formData.append('bio', this.profileForm.get('bio')?.value || '');

    if (this.selectedProfilePic) {
      formData.append('profile_picture', this.selectedProfilePic);
    }

    this.authService.update_user_profile(formData).subscribe({
      next: (res: ApiResponse) => {
        if (res.errCode === 0) {
          this.displayUser = { ...this.displayUser, ...res.datarec };
          if (this.currentUser && this.currentUser.user_id === res.datarec.user_id) {
            this.authService.setUser(res.datarec);
          }
          this.isEditMode = false;
          alert('Profile updated successfully!');
        } else {
          alert(`Update failed: ${res.message}`);
        }
      },
      error: (err) => alert('An error occurred while updating the profile.')
    });
  }

  startClose() {
    this.isClosing = true;
    setTimeout(() => this.closeProfile.emit(), 300);
  }

  logout() {
    this.authService.clearUser();
    this.router.navigate(['/login']); 
    this.startClose();
  }

  switchProfile() {
    if (this.isSuperAdmin) {
      const targetRoute = this.router.url.includes('/admin') ? '/homescreen' : '/admin';
      this.router.navigate([targetRoute]); 
    }
    this.startClose();
  }

  onBackdropClick() {
    this.startClose();
  }

  onPanelClick(event: Event) {
    event.stopPropagation();
  }
}
