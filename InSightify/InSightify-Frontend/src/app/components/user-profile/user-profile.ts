// import { Component, OnInit, Output, EventEmitter, Input } from '@angular/core';
// import { CommonModule } from '@angular/common';
// import { Router } from '@angular/router';
// import { AuthService } from '../../services/auth';
// import { CurrUser } from '../../services/api-interfaces';

// @Component({
//   selector: 'app-user-profile',
//   standalone: true,
//   imports: [CommonModule],
//   templateUrl: './user-profile.html',
//   styleUrls: ['./user-profile.css']
// })

// export class UserProfile implements OnInit {
//   @Output() closeProfile = new EventEmitter<void>();
//   currentUser: CurrUser | null = null;
//   otherUser: CurrUser | null=null;
//   isClosing = false;
//   profile_role=""
//   profile=""
//   change_navigation=""
//   isSuperAdmin=false;
//   constructor(private authService: AuthService, private router: Router) {}

//   ngOnInit() {
//     this.currentUser = this.authService.getCurrentUser();
//     this.profile_role=this.currentUser!.user_role
//     if(this.profile_role==="Super Admin") this.isSuperAdmin=true;
//     if(this.router.url.includes('/admin') && this.isSuperAdmin) {
//       this.profile="User"
//       this.change_navigation='/homescreen'
//     }
//     else if (this.router.url.includes('/homescreen') && this.isSuperAdmin){
//       this.profile="Admin"
//       this.change_navigation='/admin'
//     }
//   }

//   startClose() {
//     this.isClosing = true;
//     setTimeout(() => {
//       this.closeProfile.emit();
//     }, 300);
//   }

//   logout() {
//     this.authService.clearUser();
//     this.router.navigate(['/login']); 
//     this.startClose();
//   }

//   switchProfile() {
//     if(this.isSuperAdmin) {
//       this.router.navigate([this.change_navigation]); 
//     }
//     this.startClose();
//   }

//   onBackdropClick() {
//     this.startClose();
//   }

//   openOtherProfile(user_id: number){
//     // this.otherUser=this.authService.user_profile(user_id)
//   } 

//   onPanelClick(event: Event) {
//     event.stopPropagation();
//   }
// }

import { Component, OnInit, Output, EventEmitter, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth';
import { ApiResponse, CurrUser } from '../../services/api-interfaces';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-user-profile',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
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

  constructor(
    private authService: AuthService, 
    private router: Router,
    private fb: FormBuilder
  ) {
    this.profileForm = this.fb.group({
      bio: [''],
      profile_picture: ['']
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

  saveProfile() {
    if (!this.profileForm.valid || !this.currentUser) return;

    const payload = {
      user_id: this.currentUser.user_id,
      ...this.profileForm.value
    };

    this.authService.update_user_profile(payload).subscribe({
      next: (res: ApiResponse) => {
        if (res.errCode === 0) {
          this.displayUser = { ...this.displayUser, ...res.datarec };
          // If the updated user is the currently logged-in user, update local storage
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
