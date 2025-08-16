import { Pipe, PipeTransform } from '@angular/core';
import { environment } from '../../environments/environment';

@Pipe({
  name: 'imageUrl',
  standalone: true, // Make the pipe standalone
})
export class ImageUrlPipe implements PipeTransform {
  private readonly backendUrl = environment.apiUrl;

  transform(value: string | null | undefined): string {
    // If the value is null or empty, return a path to a default local asset
    if (!value) {
      return 'assets/profile_picture.png';
    }

    // Check if the path is already a full URL (in case some are stored differently)
    if (value.startsWith('http')) {
      return value;
    }

    // Combine the backend URL with the partial path to create the full URL
    return this.backendUrl + value;
  }
}
