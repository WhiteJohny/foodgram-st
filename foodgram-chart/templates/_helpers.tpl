{{- define "foodgram.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "foodgram.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{- define "foodgram.labels" -}}
helm.sh/chart: {{ include "foodgram.name" . }}-{{ .Chart.Version | replace "+" "_" }}
{{ include "foodgram.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "foodgram.selectorLabels" -}}
app.kubernetes.io/name: {{ include "foodgram.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{- define "foodgram.nginxDefaultConfig" -}}
server {
    listen 80;
    server_name localhost;
    client_max_body_size 10M;

    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }

    location /static/ {
        root /usr/share/nginx/html;
        try_files $uri @backend_static;
        expires 1y;
        add_header Cache-Control "public";
    }

    location @backend_static {
        internal;
        rewrite ^/static/(.*)$ /$1 break;
        root /app/static;
        expires 1y;
        add_header Cache-Control "public";
    }

    location /media/ {
        alias /app/media/;
        expires 1y;
        add_header Cache-Control "public";
    }

    location /api/ {
        proxy_set_header Host $http_host;
        proxy_pass http://{{ include "foodgram.fullname" . }}-backend:{{ .Values.backend.service.port }}/api/;

        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' '*';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, DELETE, PATCH';
            add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization';
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain; charset=utf-8';
            add_header 'Content-Length' 0;
            return 204;
        }

        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, DELETE, PATCH' always;
        add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization' always;
    }

    location /admin/ {
        proxy_set_header Host $http_host;
        proxy_pass http://{{ include "foodgram.fullname" . }}-backend:{{ .Values.backend.service.port }}/admin/;
    }

    location /r/ {
        proxy_set_header Host $http_host;
        proxy_pass http://{{ include "foodgram.fullname" . }}-backend:{{ .Values.backend.service.port }}/r/;
    }

    location /api/docs/ {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /redoc.html;
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
{{- end }}
