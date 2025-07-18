import { Routes } from '@angular/router';
import {Landing} from './pages/landing_page/landing/landing';
import {AuthPage} from './components/auth-page/auth-page';
import {Homescreen} from './pages/homescreen/homescreen';
import { UserProfile } from './pages/user-profile/user-profile';
import { AdminScreen } from './pages/admin-screen/admin-screen';

export const routes: Routes = [
  { path: '', component: Landing },
  { path: 'login', component: AuthPage },
  { path: 'homescreen', component: Homescreen },
  { path: 'profile', component: UserProfile },
  { path: 'admin', component: AdminScreen },
  // other routes...
];
