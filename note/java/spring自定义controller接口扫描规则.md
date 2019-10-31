### 自定义controller接口扫描规则
spring 中可以自定义RequestMappingHandlerMapping 的isHandler方法定制那些controller方法需要对外暴露处理request请求

实例：
假设我们有一个DemoProject的spring cloud项目，项目分两层，一层接口服务【主要是controller对外提供restful接口】，一层聚合服务【主要处理业务逻辑，提供restful接口供接口层服务调用】，为了统一维护聚合服务提供的接口，我们抽象出一层聚合接口层【jar包依赖】，主要是聚合服务对接口层提供的api接口以及交互dto,api；接口服务层依赖api 包实现对聚合服务的feign调用，聚合服务层依赖api包实现接口逻辑。这样的话启动聚合服务层，spring 会将feign api的接口和具体实现都对外暴露处理request请求，导致启动报错，提示重复的映射 Ambiguous mapping found.XXX
这个时候就要自定义RequestMappingHandlerMapping 的isHandler方法对feign接口不错接口映射处理

项目结构如下：
 * DemoProject-web：接口服务层，主要是controller对外提供restfule接口，可执行jar包
 * DemoProject-api：api层，主要是聚合服务对外提供的feign接口，包含feign接口以及dto实体
 * DemoProject-service：聚合服务层，主要实现业务逻辑，实现api层feign接口的处理业务。
```java
package com.cvsher.config;

import org.springframework.boot.autoconfigure.condition.ConditionalOnClass;
import org.springframework.boot.autoconfigure.web.servlet.WebMvcRegistrations;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.annotation.AnnotatedElementUtils;
import org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping;

import feign.Feign;

@Configuration
@ConditionalOnClass({ Feign.class })
public class RequestMappingConf {

	@Bean
	public WebMvcRegistrations feignWebRegistrations() {
		return new WebMvcRegistrations() {
			@Override
			public RequestMappingHandlerMapping getRequestMappingHandlerMapping() {
				return new RequestMappingHandlerMapping() {
					@Override
					protected boolean isHandler(Class<?> beanType) {

						boolean hasAnnotation = AnnotatedElementUtils
								.hasAnnotation(beanType, FeignClient.class);
						if (hasAnnotation && beanType.isInterface()) {
							return false;
						}
						return super.isHandler(beanType);

					}
				};
			}
		};
	}

}
```