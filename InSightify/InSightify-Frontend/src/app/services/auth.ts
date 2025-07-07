import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:5490';

  constructor(
    private http: HttpClient,
  ) {}

  private login_url: any = `${this.apiUrl}/login`
    login(payload:any){
    return this.http.post<any>(this.login_url, payload)
    }

  private signup_url: any = `${this.apiUrl}/signup`
  signup(payload:any){
    return this.http.post<any>(this.signup_url, payload)
  }

}
