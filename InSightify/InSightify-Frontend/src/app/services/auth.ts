import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { CurrUser, ApiResponse } from './api-interfaces';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:5490';
  private currentUserSubject = new BehaviorSubject<CurrUser | null>(null);
  currentUser$ = this.currentUserSubject.asObservable();

  constructor(private http: HttpClient) {
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

}