# Project Overview

This project is an **AI-powered content automation system** designed to monitor selected YouTube channels, identify newly published content, analyze that content, and transform it into social-media-ready visual content.

The system allows specific YouTube channels to be registered using their channel IDs. Once the channels are configured, the automation can scan them for videos published within the previous 24 hours.

The detected videos can then be analyzed using AI. The system processes the video's transcript and identifies the **main topic, key information, important points, and potential hooks** that can be used to communicate the content effectively to the target audience.

Based on this analysis, the automation generates a series of branded visual slides rather than a single image. These slides can form a complete carousel and can also be automatically converted into a **vertical short-form video**, allowing the same piece of content to be prepared in multiple formats.

The system also includes a trend-based workflow for Twitter/X, allowing trending topics to be used as additional content sources.

The overall project brings together **content monitoring, AI analysis, automated visual generation, video processing, scheduling, and social-media publishing infrastructure** into a single workflow.

---

# How It Works

The automation follows a multi-stage content pipeline:

**YouTube Channels → Content Detection → Transcript Extraction → AI Analysis → Hook & Information Extraction → Visual Generation → Carousel Creation → Video Conversion → Content Queue → Publishing**

### 1. Channel Configuration

The process begins in the **Channels** section.

YouTube channel names and channel IDs can be added to the system. These IDs allow the automation to identify and monitor the specific channels selected for content discovery.

<img width="1897" height="1021" alt="channel" src="https://github.com/user-attachments/assets/314d4749-b386-4847-b15c-bee65d2e1f87" />


### 2. YouTube Scanning

The dashboard provides a **Scan YouTube** function.

When triggered, the system checks the configured channels and identifies videos that were uploaded within the **last 24 hours**.

This creates the initial pool of newly published content that can be processed by the rest of the automation.

### 3. Content Analysis

After new videos are detected, the **Analyze + Generate** function begins the content-generation workflow.

The system retrieves the available transcript and processes the video's content using AI.

The analysis is designed to identify:

* The central topic of the video
* The most important information
* Key points from the content
* The strongest potential hook
* Information that can be presented to the audience
* A suitable structure for social-media content

The prompts used by the system are customized for the intended **Pakistani audience**, allowing the generated content to follow a specific audience, tone, and hook strategy.

<img width="1870" height="881" alt="image" src="https://github.com/user-attachments/assets/59d9603d-56e6-4d1f-b7fa-6b58d1c4c37e" />


### 4. Visual Content Generation

Once the content has been analyzed, the system generates visual content around the most important parts of the story.

Relevant screenshots or frames from the source video can be captured and incorporated into the visual content.

The system generates **multiple slides**, allowing a story to be presented as a carousel rather than restricting the output to a single image.

Depending on the content, a generated carousel may contain three, four, five, or more slides.

Each slide is structured to communicate a specific part of the story while maintaining the overall visual presentation of the content.



### 5. Carousel-to-Video Conversion

The automation goes one step further by converting the generated carousel into a **vertical video format**.

Instead of manually downloading individual slides and assembling them into a video, the system automatically combines the generated slides into a short-form video.

This allows the same content to be prepared for video-based platforms such as Reels and Shorts while maintaining an appropriate vertical format.

### 6. Twitter/X Trend Workflow

The project also includes a separate trend-based workflow using Twitter/X.

Trending topics can be selected as another source of content. The system can gather relevant visual material around a selected trend and use the configured content-generation prompts to create visual content around that topic.

This extends the system beyond monitoring predefined YouTube channels and allows it to respond to current trends.

<img width="1866" height="857" alt="image" src="https://github.com/user-attachments/assets/632a5917-2830-46eb-9af7-42981a9da7e3" />


### 7. Content Queue

Generated content is organized inside the **Content Queue**.

The queue provides a review stage where generated descriptions, carousel slides, and other content can be inspected before being published.

This creates a human-review step between automated generation and final publishing.

<img width="1852" height="852" alt="image" src="https://github.com/user-attachments/assets/e0ab919d-008a-460d-962f-2775f003f557" />


### 8. Social Media Publishing

The system is designed to connect the generated content with social-media publishing workflows.

It includes infrastructure for platforms such as Instagram and Facebook, while the overall architecture is designed to support additional platforms and integrations.

The goal is to reduce the amount of repetitive manual work required between discovering a story and preparing it for publication.

---

# Key Features

### 🎯 Automated YouTube Monitoring

Monitor selected YouTube channels using their channel IDs and identify newly uploaded videos within a 24-hour window.

### 🔎 Automated Content Discovery

The system automatically collects newly published content so that relevant videos can be processed without manually checking every monitored channel.

### 🧠 AI-Powered Content Analysis

Video transcripts are analyzed using AI to identify the central topic, important information, key points, and potential hooks.

### 🇵🇰 Audience-Specific Content Generation

Custom prompts guide the AI to generate content according to the intended Pakistani audience and the desired content style.

### 🪝 Hook Extraction

The system focuses on identifying the core hook of a story so that the most attention-grabbing information can be presented prominently in the generated visual content.

### 🖼️ Automated Carousel Creation

The system transforms analyzed information and relevant visual material into multi-slide carousel content.

### 🎥 Carousel-to-Video Automation

Generated carousel slides can automatically be converted into a vertical short-form video, eliminating the need to manually assemble the slides.

### 📈 Trend-Based Content Generation

Twitter/X trends can be used as additional content sources, allowing the system to generate content around relevant trending topics.

### 📋 Content Review Queue

Generated content is organized in a content queue where descriptions, visuals, and generated assets can be reviewed before publishing.

### 🔗 Social Media Integration

The system includes social-media integration infrastructure for publishing workflows and is designed to be extensible to additional platforms.

### ⚙️ End-to-End Automation


The project connects multiple stages of the content-production process:

**Discovery → Analysis → Generation → Design → Video Processing → Review → Publishing**

Rather than automating only one individual task, the project combines these stages into a connected content-production pipeline.

# Impact & Results

This automation was developed and used as part of the content-production system behind our Instagram presence, helping us scale the process of discovering, analyzing, creating, and preparing content for publication.

Through this system and the content workflow built around it, we were able to grow the Instagram account to **30,000+ subscribers/followers**.

The project helped turn what would otherwise be a highly manual content-production process into a more structured and automated workflow. Instead of manually monitoring multiple channels, researching stories, extracting key information, creating visual content, and preparing different formats, these stages could be connected through a single system.

The experience also demonstrated how AI, automation, and content systems can work together to support real-world audience growth at scale.

### Key Outcome

**30,000+ Instagram followers**

The achievement provided practical validation of the system's ability to support a real content operation rather than functioning only as a technical prototype.

<img width="296" height="1595" alt="image" src="https://github.com/user-attachments/assets/d5dcc761-f6f8-447d-a392-a9342b5d5ac8" />
