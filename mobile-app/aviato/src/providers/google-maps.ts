import { ViewChild, ElementRef, Component } from '@angular/core';
import { Connectivity } from './connectivity';
 
declare var google;
 
@Component({
  templateUrl: '../pages/map/map.html'
})
export class GoogleMaps {
 
  @ViewChild('map') mapElement: ElementRef;
  map: any;
 
  constructor(public connectivityService: Connectivity) {
 
  }
 
  ionViewDidLoad(){
    this.loadMap();
  }
 
  loadMap(){
 
    let latLng = new google.maps.LatLng(-34.9290, 138.6010);
 
    let mapOptions = {
      center: latLng,
      zoom: 15,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    }
 
    this.map = new google.maps.Map(this.mapElement.nativeElement, mapOptions);
 
  }
 
}