### java解压文件util
```java
package com.cvsher.util;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.util.Enumeration;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * zip压缩文件处理工具类
 * @author oujh5
 *
 */
public class zipUtil {
	
	private static Logger logger = LoggerFactory.getLogger(zipUtil.class);

	/**
	 * 解压文件
	 * @param zipFile	待解压文件
	 * @param targetDir 解压目标路径，绝对路径，文件夹
	 * @return
	 */
	@SuppressWarnings("rawtypes")
	public static boolean unZip(File zipFile, String targetDir){
		byte[] buff = new byte[1024];
		try (ZipFile zip = new ZipFile(zipFile)){
			//创建目标目录
			File targetFile = new File(targetDir);
			if(!targetFile.exists() || targetFile.isFile()){
				targetFile.mkdirs();
			}
			//返回zip包中所有的项，包括包中的文件夹以及文件夹中的文件或子文件夹
			Enumeration entries = zip.entries();
			while(entries.hasMoreElements()){
				ZipEntry entry = (ZipEntry) entries.nextElement();
				File entryFile = new File(targetFile.getAbsoluteFile()+File.separator+entry.getName());
				if(entry.isDirectory()){		//若是文件夹则创建文件夹
					entryFile.mkdir();
				}else{		//若是目录则创建目录，并copy entry内容
					if(!entryFile.getParentFile().exists()){
						entryFile.getParentFile().mkdirs();
					}
					if(entryFile.createNewFile()){
						try(FileOutputStream fos = new FileOutputStream(entryFile);
								InputStream in = zip.getInputStream(entry)){
							int len = -1;
							while((len = in.read(buff)) > 0){
								fos.write(buff, 0, len);
							}
						}
					}
				}
			}
		} catch (Exception e) {
			logger.error("解压文件异常", e);
		}
		return false;
    }
}
```