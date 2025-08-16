import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { CurrUser, ApiResponse } from './api-interfaces';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = environment.apiUrl;
  private currentUserSubject = new BehaviorSubject<CurrUser | null>(null);
  currentUser$ = this.currentUserSubject.asObservable();
  private get_profile_url=`${this.apiUrl}/user_profile`;
  private update_profile_url=`${this.apiUrl}/user_profile_update`;

  constructor(private http: HttpClient) {
    // **FIX: Check for and load the user from localStorage on initialization**
    const storedUser = localStorage.getItem('currentUser');
    if (storedUser) {
      this.currentUserSubject.next(JSON.parse(storedUser));
    }
  }

  getCurrentUser(): CurrUser | null {
    return this.currentUserSubject.value;
  }

  setUser(user: CurrUser) {
    this.currentUserSubject.next(user);
    localStorage.setItem('currentUser', JSON.stringify(user));
  }

  clearUser() {
    this.currentUserSubject.next(null);
    localStorage.removeItem('currentUser');
  }

  login(payload: any): Observable<ApiResponse> {
    return this.http.post<ApiResponse>(`${this.apiUrl}/login`, payload);
  }

  signup(payload: any): Observable<ApiResponse> {
    return this.http.post<ApiResponse>(`${this.apiUrl}/signup`, payload);
  }

  getSecQuestions(){
    return this.http.get<ApiResponse>(`${this.apiUrl}/security_questions`);
  }

  forgetPasswd(payload: any): Observable<ApiResponse> {
    return this.http.post<ApiResponse>(`${this.apiUrl}/forgot_password`, payload);
  }

   get_user_profile(payload: { user_id: number }): Observable<ApiResponse> {
    return this.http.get<ApiResponse>(this.get_profile_url, { params: payload });
  }

  update_user_profile(payload: any): Observable<ApiResponse> {
    return this.http.post<ApiResponse>(this.update_profile_url, payload);
  }
}