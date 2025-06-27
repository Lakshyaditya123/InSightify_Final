import { Routes } from '@angular/router';
import {Landing} from './pages/landing_page/landing/landing';
import {AuthPage} from './components/auth-page/auth-page';
import {Homescreen} from './pages/homescreen/homescreen';

export const routes: Routes = [
  { path: '', component: Landing },
  { path: 'login', component: AuthPage },
  { path: 'homescreen', component: Homescreen },
  // other routes...
];
